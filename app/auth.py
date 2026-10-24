"""Аккаунты пользователей: регистрация, вход по логину и паролю, гостевой вход.

Пароли хранятся только в виде хэша PBKDF2-SHA256 с солью (200 000 итераций).
Сессия — случайный токен в HttpOnly-cookie; на сервере хранится только его хэш.
"""
import hashlib
import hmac
import json
import re
import secrets
import threading
import time
from pathlib import Path

from .config import settings

COOKIE = "docmind_session"
SESSION_DAYS = 30
ITERATIONS = 200_000
USERNAME_RE = re.compile(r"^[A-Za-z0-9_.-]{3,32}$")


class AuthError(ValueError):
    pass


def _hash_password(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERATIONS).hex()


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


class UserStore:
    def __init__(self, path: Path):
        self.path = path
        self.lock = threading.RLock()
        self.users: dict[str, dict] = {}
        self.sessions: dict[str, dict] = {}
        if path.exists():
            data = json.loads(path.read_text("utf-8"))
            self.users = data.get("users", {})
            self.sessions = data.get("sessions", {})

    def _save(self) -> None:
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"users": self.users, "sessions": self.sessions}, ensure_ascii=False), "utf-8")
        tmp.replace(self.path)

    def _find(self, username: str) -> dict | None:
        username = username.strip().lower()
        return next((u for u in self.users.values() if u["username"] == username), None)

    def register(self, username: str, password: str, name: str = "") -> dict:
        username = username.strip().lower()
        if not USERNAME_RE.match(username):
            raise AuthError("username")
        if len(password) < 6:
            raise AuthError("password_short")
        with self.lock:
            if self._find(username):
                raise AuthError("username_taken")
            salt = secrets.token_bytes(16)
            user = {
                "id": secrets.token_hex(8),
                "username": username,
                "name": name.strip()[:60] or username,
                "salt": salt.hex(),
                "hash": _hash_password(password, salt),
                "created": time.time(),
                "guest": False,
            }
            self.users[user["id"]] = user
            self._save()
        return user

    def verify(self, username: str, password: str) -> dict:
        user = self._find(username)
        # сравнение хэшей за постоянное время; для несуществующего логина считаем хэш впустую
        salt = bytes.fromhex(user["salt"]) if user else b"\0" * 16
        candidate = _hash_password(password, salt)
        if not user or user.get("guest") or not hmac.compare_digest(candidate, user["hash"]):
            raise AuthError("invalid")
        return user

    def guest(self) -> dict:
        user = {"id": secrets.token_hex(8), "username": f"guest-{secrets.token_hex(3)}", "name": "Guest",
                "salt": "", "hash": "", "created": time.time(), "guest": True}
        with self.lock:
            self.users[user["id"]] = user
            self._save()
        return user

    def create_session(self, user: dict) -> str:
        token = secrets.token_urlsafe(32)
        with self.lock:
            now = time.time()
            self.sessions = {k: v for k, v in self.sessions.items() if v["expires"] > now}
            self.sessions[_hash_token(token)] = {"user_id": user["id"], "expires": now + SESSION_DAYS * 86400}
            self._save()
        return token

    def user_by_token(self, token: str | None) -> dict | None:
        if not token:
            return None
        session = self.sessions.get(_hash_token(token))
        if not session or session["expires"] < time.time():
            return None
        return self.users.get(session["user_id"])

    def drop_session(self, token: str | None) -> None:
        if token:
            with self.lock:
                if self.sessions.pop(_hash_token(token), None):
                    self._save()


def public_user(user: dict) -> dict:
    return {"id": user["id"], "username": user["username"], "name": user["name"], "guest": user.get("guest", False)}


users = UserStore(settings.data_dir / "users.json")
