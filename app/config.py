"""Настройки приложения: читаются из файла .env и переменных окружения."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def _bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except ValueError:
        return default


def _float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, default))
    except ValueError:
        return default


class Settings:
    app_name = "DocMind AI"

    # LLM
    llm_provider = os.getenv("LLM_PROVIDER", "openai").strip().lower()
    llm_base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1").strip().rstrip("/")
    llm_api_key = os.getenv("LLM_API_KEY", "").strip()
    llm_model = os.getenv("LLM_MODEL", "gpt-4o-mini").strip()
    llm_temperature = _float("LLM_TEMPERATURE", 0.2)
    llm_max_tokens = _int("LLM_MAX_TOKENS", 1500)
    llm_timeout = _float("LLM_TIMEOUT", 120)
    query_expansion = _bool("QUERY_EXPANSION", True)
    vision_ocr = _bool("VISION_OCR", False)

    # Telegram
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()

    # Сервер
    host = os.getenv("HOST", "0.0.0.0")
    port = _int("PORT", 8000)
    max_upload_mb = _int("MAX_UPLOAD_MB", 30)

    # RAG
    chunk_size = _int("CHUNK_SIZE", 900)
    chunk_overlap = _int("CHUNK_OVERLAP", 150)
    top_k = _int("TOP_K", 6)
    # Если все выбранные документы короче этого порога — модель получает их целиком
    full_context_chars = _int("FULL_CONTEXT_CHARS", 14000)
    history_turns = _int("HISTORY_TURNS", 4)

    # Пути
    data_dir = Path(os.getenv("DATA_DIR") or BASE_DIR / "data")
    upload_dir = data_dir / "uploads"
    store_file = data_dir / "store.json"
    tessdata_dir = BASE_DIR / "tessdata"
    web_dir = BASE_DIR / "web"

    @property
    def llm_enabled(self) -> bool:
        return bool(self.llm_api_key)


settings = Settings()
settings.upload_dir.mkdir(parents=True, exist_ok=True)
