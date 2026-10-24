"""Распознавание текста на сканах и фотографиях.

1) Tesseract OCR (локально, бесплатно) с языками kaz + rus + eng;
2) если Tesseract не установлен и VISION_OCR=true — мультимодальная LLM.
"""
import io
import logging
import shutil
from functools import lru_cache

from PIL import Image, ImageOps

from .config import settings

log = logging.getLogger(__name__)
WANTED_LANGS = ("kaz", "rus", "eng")


@lru_cache(maxsize=1)
def tesseract_path() -> str | None:
    return shutil.which("tesseract")


def _tess_config() -> str:
    if (settings.tessdata_dir / "eng.traineddata").exists():
        return f'--tessdata-dir "{settings.tessdata_dir}"'
    return ""


@lru_cache(maxsize=1)
def tesseract_langs() -> tuple[str, ...]:
    if not tesseract_path():
        return ()
    try:
        import pytesseract
        available = set(pytesseract.get_languages(config=_tess_config()))
    except Exception as exc:  # noqa: BLE001
        log.warning("Tesseract недоступен: %s", exc)
        return ()
    return tuple(lang for lang in WANTED_LANGS if lang in available)


def ocr_available() -> bool:
    return bool(tesseract_langs()) or (settings.vision_ocr and settings.llm_enabled)


def ocr_engine() -> str:
    if tesseract_langs():
        return "tesseract:" + "+".join(tesseract_langs())
    if settings.vision_ocr and settings.llm_enabled:
        return "vision-llm"
    return "none"


def _prepare(img: Image.Image) -> Image.Image:
    img = ImageOps.exif_transpose(img)
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    # Мелкие изображения увеличиваем — Tesseract лучше читает текст ~300 dpi
    if max(img.size) < 1600:
        scale = 1600 / max(img.size)
        img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    return img


def ocr_image(img: Image.Image) -> str:
    img = _prepare(img)
    langs = tesseract_langs()
    if langs:
        import pytesseract
        return pytesseract.image_to_string(img, lang="+".join(langs), config=_tess_config()).strip()
    if settings.vision_ocr and settings.llm_enabled:
        from .llm import vision_transcribe
        buf = io.BytesIO()
        img.convert("RGB").save(buf, format="PNG")
        return vision_transcribe(buf.getvalue())
    return ""


def ocr_bytes(data: bytes) -> str:
    with Image.open(io.BytesIO(data)) as img:
        return ocr_image(img)
