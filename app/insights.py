"""Режимы работы с документом помимо диалога.

  * Карта документа — хронология сроков, ключевые цифры, чек-лист требований, глоссарий;
  * Проверка знаний — тест по документу с объяснениями и ссылками на источник;
  * Доказательство — страница PDF с подсвеченными строками, на которых основан ответ.

Каждый факт привязывается к фрагменту документа (странице), чтобы его можно было проверить.
Без LLM работают упрощённые алгоритмы (регулярные выражения, тест «вставьте число»).
"""
import math
import random
import re

from . import llm
from .chunker import split_sentences
from .config import settings
from .lang import LANG_NAMES, format_loc
from .rag import _parse_json
from .retriever import tokenize
from .store import store

MAX_ITEMS = 8


# ---------------------------------------------------------------- общее

def _doc_text(doc: dict, budget: int = 14000) -> tuple[str, list[dict]]:
    chunks = store.doc_chunks({doc["id"]})
    picked = chunks
    if sum(len(c["text"]) for c in chunks) > budget:
        step = max(1, math.ceil(len(chunks) / (budget // settings.chunk_size)))
        picked = chunks[::step]
    return "\n\n".join(c["text"] for c in picked)[:budget], chunks


def _locate(quote: str, chunks: list[dict], lang: str) -> dict:
    """Находит фрагмент документа, из которого взята цитата → страница для ссылки."""
    q = set(tokenize(quote or ""))
    best, best_score = None, 0.0
    for chunk in chunks:
        if not q:
            break
        score = len(q & set(tokenize(chunk["text"]))) / len(q)
        if score > best_score:
            best, best_score = chunk, score
    if not best or best_score < 0.3:
        return {}
    return {"chunk_id": best["id"], "loc": best["loc"], "loc_label": format_loc(best["loc"], lang)}


def _attach(items: list, chunks: list[dict], lang: str) -> list:
    out = []
    for item in items[:MAX_ITEMS]:
        if isinstance(item, dict):
            item.update(_locate(item.get("quote", ""), chunks, lang))
            out.append(item)
    return out


async def _ask_json(prompt: str, doc: dict, text: str, max_tokens: int = 2500) -> dict | None:
    if not settings.llm_enabled:
        return None
    try:
        reply = await llm.complete(prompt, [{"role": "user", "content": f"Document: {doc['name']}\n\n{text}"}],
                                   max_tokens=max_tokens, temperature=0.3)
    except llm.LLMError:
        return None
    return _parse_json(reply)


# ---------------------------------------------------------------- карта документа

INSIGHTS_PROMPT = """You are a document analyst. Analyze the document and respond in {lang_name}.
Return ONLY valid JSON:
{{"title": "<short title of the document>",
  "summary": "<2-3 sentences: what this document is and why it matters>",
  "timeline": [{{"date": "<date or deadline>", "event": "<what happens>", "quote": "<exact phrase from the document>"}}],
  "numbers": [{{"value": "<number with unit, e.g. 3 people, 40 points, 24 months>", "label": "<what it means>", "quote": "<exact phrase>"}}],
  "requirements": [{{"text": "<one requirement / rule / obligation, short>", "quote": "<exact phrase>"}}],
  "terms": [{{"term": "<term, abbreviation or name>", "definition": "<short explanation>"}}]}}
Rules: up to 8 items per list, most important first; timeline sorted chronologically; empty list if nothing fits.
Every "quote" MUST be copied word-for-word from the document in its ORIGINAL language (5-15 words)."""

MONTHS = (r"қаңтар\w*|ақпан\w*|наурыз\w*|сәуір\w*|мамыр\w*|маусым\w*|шілде\w*|тамыз\w*|қыркүйек\w*|қазан\w*|"
          r"қараша\w*|желтоқсан\w*|январ\w*|феврал\w*|март\w*|апрел\w*|ма[йя]\w*|июн\w*|июл\w*|август\w*|"
          r"сентябр\w*|октябр\w*|ноябр\w*|декабр\w*|january|february|march|april|may|june|july|august|"
          r"september|october|november|december")
DATE_RE = re.compile(rf"(\d{{1,2}}\s+(?:{MONTHS})(?:\s+\d{{4}})?|\d{{4}}\s+жылғы\s+\d{{1,2}}\s+(?:{MONTHS})|"
                     rf"\d{{1,2}}[./]\d{{1,2}}[./]\d{{2,4}})", re.I)
NUMBER_RE = re.compile(r"(\d+(?:[.,]\d+)?(?:\s*[–-]\s*\d+)?)\s*(балл\w*|минут\w*|жас\w*|адам\w*|мүше\w*|бет\w*|"
                       r"месяц\w*|дн[ея]\w*|лет|год\w*|%|метр\w*|дБА|МБ|сағат\w*|күн\w*|смен\w*|points?|minutes?)", re.I)
REQ_RE = re.compile(r"\b(тиіс|қажет|міндетті|жол берілмейді|рұқсат етіледі|должен|должны|обязан\w*|запрещ\w*|"
                    r"необходимо|допускаются|must|required|shall|prohibited)\b", re.I)


def _offline_insights(doc: dict, chunks: list[dict], lang: str) -> dict:
    sentences = []
    for chunk in chunks:
        for s in split_sentences(chunk["text"]):
            if len(s) > 15:
                sentences.append((s, chunk))
    timeline, numbers, requirements, seen = [], [], [], set()
    for s, chunk in sentences:
        loc = {"chunk_id": chunk["id"], "loc": chunk["loc"], "loc_label": format_loc(chunk["loc"], lang)}
        short = s if len(s) < 160 else s[:157] + "…"
        m = DATE_RE.search(s)
        if m and len(timeline) < MAX_ITEMS and s not in seen:
            timeline.append({"date": m.group(0), "event": short, "quote": s, **loc})
            seen.add(s)
            continue
        m = NUMBER_RE.search(s)
        if m and len(numbers) < MAX_ITEMS and s not in seen:
            numbers.append({"value": f"{m.group(1)} {m.group(2)}", "label": short, "quote": s, **loc})
            seen.add(s)
            continue
        if REQ_RE.search(s) and len(requirements) < MAX_ITEMS and s not in seen:
            requirements.append({"text": short, "quote": s, **loc})
            seen.add(s)
    first = next((s for s, _ in sentences), doc["name"])
    return {"title": doc["name"], "summary": first[:300], "timeline": timeline, "numbers": numbers,
            "requirements": requirements, "terms": [], "offline": True}


async def insights(doc: dict, lang: str) -> dict:
    key = f"insights:{lang}"
    if doc.get("cache", {}).get(key):
        return doc["cache"][key]
    text, chunks = _doc_text(doc)
    data = await _ask_json(INSIGHTS_PROMPT.format(lang_name=LANG_NAMES[lang]), doc, text)
    if not data or not isinstance(data, dict):
        return _offline_insights(doc, chunks, lang)
    result = {
        "title": str(data.get("title") or doc["name"]),
        "summary": str(data.get("summary") or ""),
        "timeline": _attach(data.get("timeline") or [], chunks, lang),
        "numbers": _attach(data.get("numbers") or [], chunks, lang),
        "requirements": _attach(data.get("requirements") or [], chunks, lang),
        "terms": [t for t in (data.get("terms") or []) if isinstance(t, dict)][:MAX_ITEMS],
    }
    store.set_cache(doc["id"], key, result)
    return result


# ---------------------------------------------------------------- проверка знаний

QUIZ_PROMPT = """You create a knowledge test based ONLY on the document. Respond in {lang_name}.
Return ONLY valid JSON:
{{"questions": [{{"question": "<question>", "options": ["<A>", "<B>", "<C>", "<D>"], "answer": <index 0-3 of the correct option>,
  "explanation": "<1-2 sentences why it is correct>", "quote": "<exact phrase from the document proving the answer, original language>"}}]}}
Create exactly {n} questions about the most important facts, rules and numbers. Distractors must be plausible.
Vary the position of the correct answer. Every question must be answerable from the document."""

NUM_TOKEN = re.compile(r"\b\d+(?:[.,]\d+)?\b")


def _offline_quiz(chunks: list[dict], lang: str, n: int) -> list[dict]:
    """Тест без LLM: в предложении с числом число заменяется пропуском, варианты — правильное и похожие числа."""
    prompts = {"kk": "Бос орынды толтырыңыз:", "ru": "Заполните пропуск:", "en": "Fill in the blank:"}
    explain = {"kk": "Құжатта:", "ru": "В документе:", "en": "The document says:"}
    candidates = []
    for chunk in chunks:
        for s in split_sentences(chunk["text"]):
            # только числа с единицей измерения (баллы, минуты, месяцы) — не годы, телефоны и номера пунктов
            m = NUMBER_RE.search(s)
            if m and 30 < len(s) < 260 and NUM_TOKEN.fullmatch(m.group(1)):
                candidates.append((s, m.group(1), chunk))
    rng = random.Random()
    rng.shuffle(candidates)
    questions = []
    for s, num, chunk in candidates[:n]:
        value = float(num.replace(",", "."))
        options = [num]
        for alt in (value + 1, value * 2, value - 1, value + 5, value + 2, value + 10):
            label = str(int(alt)) if alt == int(alt) else f"{alt:g}"
            if alt > 0 and label not in options and len(options) < 4:
                options.append(label)
        rng.shuffle(options)
        blanked = re.sub(rf"\b{re.escape(num)}\b", "_____", s, count=1)
        questions.append({
            "question": f"{prompts[lang]} {blanked}",
            "options": options,
            "answer": options.index(num),
            "explanation": f"{explain[lang]} «{s}»",
            "quote": s,
            "chunk_id": chunk["id"], "loc": chunk["loc"], "loc_label": format_loc(chunk["loc"], lang),
        })
    return questions


async def quiz(doc: dict, lang: str, n: int = 5) -> dict:
    text, chunks = _doc_text(doc)
    data = await _ask_json(QUIZ_PROMPT.format(lang_name=LANG_NAMES[lang], n=n), doc, text, max_tokens=3000)
    questions = []
    for q in (data or {}).get("questions", []) if isinstance(data, dict) else []:
        try:
            options = [str(o) for o in q["options"]][:4]
            answer = int(q["answer"])
        except (KeyError, TypeError, ValueError):
            continue
        if len(options) < 2 or not 0 <= answer < len(options):
            continue
        item = {"question": str(q.get("question", "")), "options": options, "answer": answer,
                "explanation": str(q.get("explanation", "")), "quote": str(q.get("quote", ""))}
        item.update(_locate(item["quote"], chunks, lang))
        questions.append(item)
    if questions:
        return {"questions": questions[:n]}
    return {"questions": _offline_quiz(chunks, lang, n), "offline": True}


# ---------------------------------------------------------------- доказательство на странице

def _key_lines(chunk_text: str, query: str) -> list[set[str]]:
    """Предложения фрагмента, которые лучше всего совпадают с вопросом/ответом — их и подсвечиваем."""
    q = set(tokenize(query))
    scored = []
    # переносы строк PDF внутри предложения убираем, чтобы подсветить предложение целиком
    for s in re.split(r"(?<=[.!?…;])\s+", chunk_text.replace("\n", " ")):
        tokens = set(tokenize(s))
        if len(tokens) >= 2:
            scored.append((len(tokens & q), tokens))
    if not scored:
        return []
    best = max(score for score, _ in scored)
    if best == 0:
        return []
    return [tokens for score, tokens in scored if score >= max(1, best * 0.5)]


def render_evidence(doc: dict, chunk: dict, query: str) -> bytes | None:
    """PNG страницы PDF с жёлтой подсветкой строк, на которых основан ответ."""
    if doc["ext"] != ".pdf" or chunk["loc"].get("type") != "page":
        return None
    import pymupdf

    targets = _key_lines(chunk["text"], query)
    with pymupdf.open(store.file_path(doc)) as pdf:
        page = pdf[int(chunk["loc"]["value"]) - 1]
        data = page.get_text("dict")
        for block in data.get("blocks", []):
            for line in block.get("lines", []):
                line_text = "".join(span["text"] for span in line.get("spans", []))
                tokens = set(tokenize(line_text))
                if len(tokens) < 2:
                    continue
                if any(len(tokens & t) / len(tokens) >= 0.6 for t in targets):
                    annot = page.add_highlight_annot(pymupdf.Rect(line["bbox"]))
                    annot.set_colors(stroke=(1.0, 0.85, 0.2))
                    annot.update()
        return page.get_pixmap(dpi=110).tobytes("png")
