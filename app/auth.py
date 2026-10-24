"""Аккаунты: регистрация по email с подтверждением кодом, вход, сброс пароля, настройки.

Безопасность:
  * пароль — минимум 8 символов, буквы и цифры; хранится только хэш PBKDF2-SHA256 с солью;
  * email подтверждается 6-значным кодом (10 минут, не больше 5 попыток), коды хранятся хэшированными;
  * Gmail-алиасы (точки и +метки) считаются одним адресом — нельзя завести 10 аккаунтов на один ящик;
  * одноразовые почтовые сервисы запрещены;
  * лимиты по IP на регистрацию, вход, гостевые аккаунты и отправку кодов;
  * 5 неверных паролей подряд — вход в аккаунт блокируется на 15 минут;
  * ответы «забыли пароль» не раскрывают, существует ли такой email;
  * сессия — случайный токен в HttpOnly-cookie, на сервере хранится только его хэш;
    после смены/сброса пароля все сессии завершаются.
"""
import hashlib
import hmac
import json
import re
import secrets
import threading
import time
from collections import defaultdict, deque
from pathlib import Path

from .config import settings

COOKIE = "docmind_session"
SESSION_DAYS = 30
ITERATIONS = 200_000
CODE_TTL = 10 * 60
CODE_ATTEMPTS = 5
RESEND_COOLDOWN = 60
LOCK_AFTER = 5
LOCK_SECONDS = 15 * 60

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]{1,64}@[A-Za-z0-9.-]+\.[A-Za-z]{2,24}$")
DISPOSABLE = {
    "mailinator.com", "10minutemail.com", "10minutemail.net", "tempmail.com", "temp-mail.org", "temp-mail.io",
    "guerrillamail.com", "guerrillamail.net", "sharklasers.com", "yopmail.com", "yopmail.net", "trashmail.com",
    "getnada.com", "nada.email", "dispostable.com", "maildrop.cc", "fakeinbox.com", "mintemail.com",
    "throwawaymail.com", "mohmal.com", "emailondeck.com", "tempinbox.com", "mailnesia.com", "tempr.email",
    "discard.email", "spamgourmet.com", "mailcatch.com", "burnermail.io", "moakt.com", "tmpmail.org",
    "tmail.ws", "inboxkitten.com", "1secmail.com", "1secmail.net", "emailfake.com", "crazymailing.com",
}
DEFAULT_SETTINGS = {
    "theme": "system",          # system | light | dark | sepia | midnight
    "accent": "indigo",         # graphite | indigo | emerald | ocean | amber | rose
    "font": "m",                # s | m | l
    "width": "normal",          # normal | wide
    "ui_lang": "auto",          # auto | kk | ru | en
    "answer_lang": "auto",      # auto | kk | ru | en
    "answer_style": "balanced",  # concise | balanced | detailed
    "answer_model": "lite",      # lite | pro (Mind Pro смотрит на страницы PDF)
    "show_sources": True,
    "show_trust": True,
    "suggestions": True,
}
SETTING_CHOICES = {
    "theme": {"system", "light", "dark", "sepia", "midnight"},
    "accent": {"graphite", "indigo", "emerald", "ocean", "amber", "rose"}, "font": {"s", "m", "l"}, "width": {"normal", "wide"},
    "ui_lang": {"auto", "kk", "ru", "en"},
    "answer_lang": {"auto", "kk", "ru", "en"}, "answer_style": {"concise", "balanced", "detailed"},
    "answer_model": {"lite", "pro"},
}
LIMITS = {  # действие: (максимум, окно в секундах) — на один IP (с запасом для общего Wi-Fi на площадке)
    "register": (15, 3600),
    "login": (40, 600),
    "code": (20, 3600),
}


class AuthError(ValueError):
    """Код ошибки (строка) переводится на странице входа."""


def _hash_password(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERATIONS).hex()


def _sha(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def normalize_email(email: str) -> str:
    """Канонический вид адреса: регистр, Gmail-точки и +метки не создают «новых» ящиков."""
    email = email.strip().lower()
    local, _, domain = email.partition("@")
    local = local.split("+", 1)[0]
    if domain in ("gmail.com", "googlemail.com"):
        local, domain = local.replace(".", ""), "gmail.com"
    return f"{local}@{domain}"


def check_email(email: str) -> None:
    if not EMAIL_RE.match(email.strip()):
        raise AuthError("email_invalid")
    domain = email.strip().lower().rsplit("@", 1)[1]
    if domain in DISPOSABLE or any(domain.endswith("." + d) for d in DISPOSABLE):
        raise AuthError("email_disposable")


def check_password(password: str, email: str = "") -> None:
    if len(password) < 8:
        raise AuthError("password_short")
    if not re.search(r"[^\W\d_]", password) or not re.search(r"\d", password):
        raise AuthError("password_weak")
    if email and password.lower() in email.lower():
        raise AuthError("password_weak")


class RateLimiter:
    def __init__(self):
        self.events: dict[tuple[str, str], deque] = defaultdict(deque)
        self.lock = threading.Lock()

    def hit(self, action: str, key: str) -> None:
        limit, window = LIMITS[action]
        now = time.time()
        with self.lock:
            q = self.events[(action, key)]
            while q and q[0] < now - window:
                q.popleft()
            if len(q) >= limit:
                raise AuthError("too_many")
            q.append(now)


limiter = RateLimiter()


class UserStore:
    def __init__(self, path: Path):
        self.path = path
        self.lock = threading.RLock()
        self.users: dict[str, dict] = {}
        self.sessions: dict[str, dict] = {}
        if path.exists():
            data = json.loads(path.read_text("utf-8"))
            # аккаунты старого формата (без email) не переносим
            # гостевой режим отключён: остаются только аккаунты с email
            self.users = {k: u for k, u in data.get("users", {}).items() if "email" in u and not u.get("guest")}
            self.sessions = {k: s for k, s in data.get("sessions", {}).items() if s["user_id"] in self.users}

    def _save(self) -> None:
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"users": self.users, "sessions": self.sessions}, ensure_ascii=False), "utf-8")
        tmp.replace(self.path)

    def find(self, email: str) -> dict | None:
        key = normalize_email(email)
        return next((u for u in self.users.values() if u.get("email_key") == key), None)

    # ---------- коды подтверждения

    def _issue_code(self, user: dict, kind: str) -> str:
        last = user.get("code", {})
        if last.get("kind") == kind and time.time() - last.get("sent", 0) < RESEND_COOLDOWN:
            raise AuthError("wait")
        code = f"{secrets.randbelow(1_000_000):06d}"
        user["code"] = {"kind": kind, "hash": _sha(user["id"] + code), "expires": time.time() + CODE_TTL,
                        "attempts": 0, "sent": time.time()}
        self._save()
        return code

    def _check_code(self, user: dict, kind: str, code: str) -> None:
        c = user.get("code") or {}
        if c.get("kind") != kind or c.get("expires", 0) < time.time():
            raise AuthError("code_expired")
        if c["attempts"] >= CODE_ATTEMPTS:
            raise AuthError("code_expired")
        c["attempts"] += 1
        if not hmac.compare_digest(c["hash"], _sha(user["id"] + code.strip())):
            self._save()
            raise AuthError("code_invalid")
        user.pop("code", None)

    # ---------- регистрация и вход

    def register(self, name: str, email: str, password: str) -> tuple[dict, str | None]:
        email = email.strip()
        check_email(email)
        name = re.sub(r"\s+", " ", name).strip()[:60]
        if len(name) < 2:
            raise AuthError("name_invalid")
        check_password(password, email)
        with self.lock:
            existing = self.find(email)
            if existing and existing.get("verified"):
                raise AuthError("email_taken")
            if existing:  # не подтверждённая ранее регистрация — перезаписываем
                self.users.pop(existing["id"], None)
            salt = secrets.token_bytes(16)
            user = {
                "id": secrets.token_hex(8), "email": email.lower(), "email_key": normalize_email(email),
                "name": name, "salt": salt.hex(), "hash": _hash_password(password, salt),
                "verified": False, "guest": False, "created": time.time(),
                "failed": 0, "locked_until": 0, "settings": dict(DEFAULT_SETTINGS),
            }
            self.users[user["id"]] = user
            code = self._issue_code(user, "verify")
        return user, code

    def verify_email(self, email: str, code: str) -> dict:
        with self.lock:
            user = self.find(email)
            if not user or user.get("verified"):
                raise AuthError("code_invalid")
            self._check_code(user, "verify", code)
            user["verified"] = True
            self._save()
            return user

    def resend(self, email: str, kind: str) -> tuple[dict, str] | None:
        """Повторная отправка кода. None — если адрес неизвестен (не раскрываем это наружу)."""
        with self.lock:
            user = self.find(email)
            if not user or user.get("guest"):
                return None
            if kind == "verify" and user.get("verified"):
                return None
            if kind == "reset" and not user.get("verified"):
                return None
            return user, self._issue_code(user, kind)

    def login(self, email: str, password: str) -> dict:
        with self.lock:
            user = self.find(email)
            salt = bytes.fromhex(user["salt"]) if user else b"\0" * 16
            candidate = _hash_password(password, salt)  # считаем хэш всегда — время ответа одинаковое
            if not user or user.get("guest"):
                raise AuthError("invalid")
            if user.get("locked_until", 0) > time.time():
                raise AuthError("locked")
            if not hmac.compare_digest(candidate, user["hash"]):
                user["failed"] = user.get("failed", 0) + 1
                if user["failed"] >= LOCK_AFTER:
                    user["failed"], user["locked_until"] = 0, time.time() + LOCK_SECONDS
                self._save()
                raise AuthError("invalid")
            user["failed"] = 0
            if not user.get("verified"):
                raise AuthError("not_verified")
            self._save()
            return user

    def reset_password(self, email: str, code: str, password: str) -> dict:
        with self.lock:
            user = self.find(email)
            if not user or not user.get("verified"):
                raise AuthError("code_invalid")
            self._check_code(user, "reset", code)
            check_password(password, user["email"])
            self._set_password(user, password)
            return user

    def change_password(self, user: dict, old: str, new: str) -> None:
        with self.lock:
            if not hmac.compare_digest(_hash_password(old, bytes.fromhex(user["salt"])), user["hash"]):
                raise AuthError("invalid")
            check_password(new, user["email"])
            self._set_password(user, new)

    def _set_password(self, user: dict, password: str) -> None:
        salt = secrets.token_bytes(16)
        user["salt"], user["hash"] = salt.hex(), _hash_password(password, salt)
        user["failed"], user["locked_until"] = 0, 0
        # все старые сессии больше не действуют
        self.sessions = {k: s for k, s in self.sessions.items() if s["user_id"] != user["id"]}
        self._save()

    def firebase_login(self, uid: str, email: str, name: str) -> dict:
        """Вход через Firebase (email-ссылка или Google). Почта уже подтверждена Firebase."""
        check_email(email)
        with self.lock:
            user = next((u for u in self.users.values() if u.get("firebase_uid") == uid), None)
            if not user:
                same = self.find(email)
                if same and same.get("firebase_uid") not in (None, uid):
                    raise AuthError("email_taken")  # тот же ящик (с учётом Gmail-алиасов) уже у другого аккаунта
                user = same
            if not user:
                user = {"id": secrets.token_hex(8), "email": email.lower(), "email_key": normalize_email(email),
                        "name": (re.sub(r"\s+", " ", name).strip() or email.split("@")[0])[:60],
                        "salt": "", "hash": "", "verified": True, "guest": False, "created": time.time(),
                        "failed": 0, "locked_until": 0, "settings": dict(DEFAULT_SETTINGS)}
                self.users[user["id"]] = user
            user["firebase_uid"], user["verified"] = uid, True
            self._save()
            return user

    def email_available(self, email: str) -> None:
        """Проверка до создания аккаунта в Firebase: формат, одноразовые ящики, Gmail-алиасы."""
        check_email(email)
        user = self.find(email)  # find учитывает Gmail-алиасы: a.b+1@gmail.com = ab@gmail.com
        if user and user.get("verified"):
            raise AuthError("email_taken")

    def delete(self, user: dict) -> None:
        with self.lock:
            self.users.pop(user["id"], None)
            self.sessions = {k: s for k, s in self.sessions.items() if s["user_id"] != user["id"]}
            self._save()

    # ---------- профиль и настройки

    def update_profile(self, user: dict, name: str) -> None:
        name = re.sub(r"\s+", " ", name).strip()[:60]
        if len(name) < 2:
            raise AuthError("name_invalid")
        with self.lock:
            user["name"] = name
            self._save()

    def update_settings(self, user: dict, values: dict) -> dict:
        with self.lock:
            current = {**DEFAULT_SETTINGS, **user.get("settings", {})}
            for key, value in values.items():
                if key in SETTING_CHOICES and value in SETTING_CHOICES[key]:
                    current[key] = value
                elif key in DEFAULT_SETTINGS and isinstance(DEFAULT_SETTINGS[key], bool) and isinstance(value, bool):
                    current[key] = value
            user["settings"] = current
            self._save()
            return current

    # ---------- сессии

    def create_session(self, user: dict) -> str:
        token = secrets.token_urlsafe(32)
        with self.lock:
            now = time.time()
            self.sessions = {k: v for k, v in self.sessions.items() if v["expires"] > now}
            self.sessions[_sha(token)] = {"user_id": user["id"], "expires": now + SESSION_DAYS * 86400}
            self._save()
        return token

    def user_by_token(self, token: str | None) -> dict | None:
        if not token:
            return None
        session = self.sessions.get(_sha(token))
        if not session or session["expires"] < time.time():
            return None
        user = self.users.get(session["user_id"])
        return user if user and user.get("verified") and not user.get("guest") else None

    def drop_session(self, token: str | None) -> None:
        if token:
            with self.lock:
                if self.sessions.pop(_sha(token), None):
                    self._save()


def public_user(user: dict) -> dict:
    return {
        "id": user["id"], "name": user["name"], "email": user.get("email", ""), "guest": user.get("guest", False),
        "provider": "firebase" if user.get("firebase_uid") and not user.get("hash") else "password",
        "plan": user.get("plan", "free"),  # free | pro — Mind Pro будет по подписке
        "settings": {**DEFAULT_SETTINGS, **user.get("settings", {})},
    }


users = UserStore(settings.data_dir / "users.json")
