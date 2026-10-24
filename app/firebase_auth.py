"""Проверка ID-токенов Firebase Authentication на сервере (подпись Google, проект, срок действия)."""
from __future__ import annotations

from functools import lru_cache

from .config import settings


def enabled() -> bool:
    return bool(settings.firebase_api_key and settings.firebase_project_id)


def public_config() -> dict | None:
    if not enabled():
        return None
    return {"apiKey": settings.firebase_api_key, "authDomain": settings.firebase_auth_domain or f"{settings.firebase_project_id}.firebaseapp.com",
            "projectId": settings.firebase_project_id, "appId": settings.firebase_app_id}


@lru_cache(maxsize=1)
def _request():
    import google.auth.transport.requests
    import requests
    return google.auth.transport.requests.Request(session=requests.Session())  # ключи Google кешируются в сессии


def verify(id_token: str) -> dict:
    """Возвращает данные пользователя из токена. Бросает ValueError, если токен поддельный или просрочен."""
    from google.oauth2 import id_token as google_id_token
    claims = google_id_token.verify_firebase_token(id_token, _request(), audience=settings.firebase_project_id)
    if not claims or not claims.get("email"):
        raise ValueError("no email")
    provider = (claims.get("firebase") or {}).get("sign_in_provider", "")
    if not claims.get("email_verified") and provider != "google.com":
        raise ValueError("not_verified")
    return claims
