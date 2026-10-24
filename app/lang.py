"""Определение языка (казахский / русский / английский) и локализованные строки."""
import re

KK_LETTERS = set("әғқңөұүһіӘҒҚҢӨҰҮҺІ")
_CYR = re.compile(r"[а-яёА-ЯЁ]")
_LAT = re.compile(r"[a-zA-Z]")

LANG_NAMES = {"kk": "Kazakh (қазақ тілі)", "ru": "Russian (русский язык)", "en": "English"}


# Частые казахские слова, в которых нет особых букв («Командада неше адам болады?»)
KK_WORDS = {"неше", "болады", "болса", "бола", "керек", "мен", "бен", "пен", "туралы", "бойынша", "деген",
            "бар", "ма", "ме", "ба", "бе", "па", "пе", "адам", "немесе", "дейін", "кейін", "арқылы", "тиіс"}
_WORD = re.compile(r"[а-яёәғқңөұүһі]+", re.I)


def detect_lang(text: str, default: str = "ru") -> str:
    """Казахские буквы (ә, ғ, қ, ң, ө, ұ, ү, һ, і) не встречаются в русском — это надёжный признак."""
    if not text:
        return default
    if any(ch in KK_LETTERS for ch in text):
        return "kk"
    if any(w in KK_WORDS for w in _WORD.findall(text.lower())):
        return "kk"
    cyr = len(_CYR.findall(text))
    lat = len(_LAT.findall(text))
    if cyr == 0 and lat == 0:
        return default
    return "ru" if cyr >= lat else "en"


STRINGS = {
    "no_docs": {
        "kk": "Әзірге бірде-бір құжат жүктелмеген. Алдымен PDF, DOCX немесе басқа құжатты жүктеңіз, содан кейін сұрақ қойыңыз.",
        "ru": "Пока не загружено ни одного документа. Сначала загрузите PDF, DOCX или другой документ, затем задайте вопрос.",
        "en": "No documents uploaded yet. Please upload a PDF, DOCX or another document first, then ask your question.",
    },
    "not_found": {
        "kk": "Кешіріңіз, жүктелген құжаттардан бұл сұраққа жауап таба алмадым.",
        "ru": "К сожалению, в загруженных документах не нашлось ответа на этот вопрос.",
        "en": "Sorry, I could not find an answer to this question in the uploaded documents.",
    },
    "offline_note": {
        "kk": "_Офлайн режим: LLM қосылмаған, құжаттан ең сәйкес үзінділер көрсетілді._",
        "ru": "_Офлайн-режим: LLM не подключена, показаны самые релевантные фрагменты документа._",
        "en": "_Offline mode: no LLM connected, showing the most relevant passages from the documents._",
    },
    "llm_error": {
        "kk": "LLM сервисіне қосылу мүмкін болмады. Төменде құжаттан табылған үзінділер берілген.",
        "ru": "Не удалось обратиться к LLM-сервису. Ниже — фрагменты, найденные в документах.",
        "en": "Could not reach the LLM service. Below are the passages found in the documents.",
    },
    "loc_page": {"kk": "бет", "ru": "стр.", "en": "p."},
    "loc_slide": {"kk": "слайд", "ru": "слайд", "en": "slide"},
    "loc_sheet": {"kk": "парақ", "ru": "лист", "en": "sheet"},
    "loc_section": {"kk": "бөлім", "ru": "раздел", "en": "section"},
    "loc_image": {"kk": "сурет", "ru": "изображение", "en": "image"},
}


def t(key: str, lang: str) -> str:
    variants = STRINGS[key]
    return variants.get(lang) or variants["ru"]


def format_loc(loc: dict, lang: str) -> str:
    kind = loc.get("type", "section")
    value = loc.get("value")
    if kind == "image" or value in (None, ""):
        return t("loc_image", lang) if kind == "image" else ""
    return f"{t('loc_' + kind, lang)} {value}"
