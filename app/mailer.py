"""Отправка писем с кодами подтверждения.

Если в .env задан SMTP (например, Gmail с паролем приложения) — письмо уходит на почту.
Иначе (режим разработки) код печатается в консоль сервера и сохраняется в outbox для автотестов.
"""
import logging
import smtplib
import ssl
from email.message import EmailMessage

from .config import settings

log = logging.getLogger(__name__)
outbox: list[dict] = []  # последние письма в режиме разработки

SUBJECTS = {
    "verify": {"kk": "Mind AI: тіркелуді растау коды", "ru": "Mind AI: код подтверждения", "en": "Mind AI: verification code"},
    "reset": {"kk": "Mind AI: құпиясөзді қалпына келтіру", "ru": "Mind AI: сброс пароля", "en": "Mind AI: password reset"},
}
BODIES = {
    "verify": {
        "kk": "Сәлем, {name}!\n\nТіркелуді растау коды: {code}\nКод 10 минут жарамды.\n\nЕгер сіз тіркелмеген болсаңыз, бұл хатты елемеңіз.",
        "ru": "Здравствуйте, {name}!\n\nКод подтверждения регистрации: {code}\nКод действует 10 минут.\n\nЕсли вы не регистрировались — просто проигнорируйте письмо.",
        "en": "Hi {name}!\n\nYour verification code: {code}\nThe code is valid for 10 minutes.\n\nIf you did not sign up, just ignore this email.",
    },
    "reset": {
        "kk": "Сәлем, {name}!\n\nҚұпиясөзді қалпына келтіру коды: {code}\nКод 10 минут жарамды.\n\nЕгер сұрау сізден болмаса, құпиясөзіңіз өзгермейді.",
        "ru": "Здравствуйте, {name}!\n\nКод для сброса пароля: {code}\nКод действует 10 минут.\n\nЕсли вы не запрашивали сброс — пароль останется прежним.",
        "en": "Hi {name}!\n\nYour password reset code: {code}\nThe code is valid for 10 minutes.\n\nIf you did not request this, your password stays the same.",
    },
}


def mode() -> str:
    return "smtp" if settings.smtp_host and settings.smtp_user else "console"


def send_code(to: str, kind: str, code: str, name: str, lang: str = "ru") -> None:
    lang = lang if lang in ("kk", "ru", "en") else "ru"
    subject = SUBJECTS[kind][lang]
    body = BODIES[kind][lang].format(name=name or to, code=code)
    if mode() == "console":
        outbox.append({"to": to, "kind": kind, "code": code})
        del outbox[:-50]
        log.warning("📧 [режим разработки] %s для %s: КОД %s", kind, to, code)
        return
    msg = EmailMessage()
    msg["From"] = settings.smtp_from or settings.smtp_user
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    if settings.smtp_port == 465:
        with smtplib.SMTP_SSL(settings.smtp_host, 465, context=ssl.create_default_context(), timeout=20) as s:
            s.login(settings.smtp_user, settings.smtp_password)
            s.send_message(msg)
    else:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=20) as s:
            s.starttls(context=ssl.create_default_context())
            s.login(settings.smtp_user, settings.smtp_password)
            s.send_message(msg)
