"""Режимы работы с документом помимо диалога.

  * Карта документа — хронология сроков, ключевые цифры, чек-лист требований, глоссарий;
  * Проверка знаний — тест по документу с объяснениями и ссылками на источник (каждый раз новые вопросы);
  * Карточки — вопрос на лицевой стороне, ответ на обороте, для запоминания;
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

MAX_ITEMS = 14
MAP_BUDGET = 40000  # документ до ~40 тыс. символов карта видит целиком — иначе теряются целые разделы


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


def _random_text(chunks: list[dict], budget: int = 14000) -> str:
    """Для теста и карточек: случайная часть длинного документа — каждый раз вопросы по другим местам."""
    if sum(len(c["text"]) for c in chunks) <= budget:
        return "\n\n".join(c["text"] for c in chunks)
    picked = random.sample(chunks, k=min(len(chunks), max(1, budget // settings.chunk_size)))
    picked.sort(key=lambda c: c["idx"])
    return "\n\n".join(c["text"] for c in picked)[:budget]


def _seen(doc: dict, key: str) -> list[str]:
    return list(doc.get("cache", {}).get(key) or [])


def _remember(doc: dict, key: str, items: list[str], keep: int = 40) -> None:
    store.set_cache(doc["id"], key, (_seen(doc, key) + items)[-keep:])


def _avoid(seen: list[str]) -> str:
    if not seen:
        return ""
    listed = "\n".join(f"- {q}" for q in seen[-25:])
    return f"\n\nThe user has ALREADY seen these — ask about OTHER facts, do not repeat or rephrase them:\n{listed}"


def _fresh_first(items: list[dict], key: str, seen: list[str], n: int) -> list[dict]:
    """Сначала — вопросы, не похожие на уже заданные; повторы только если новых не хватает."""
    seen_tokens = [set(tokenize(q)) for q in seen]

    def repeated(text: str) -> bool:
        t = set(tokenize(text))
        return any(t and len(t & s) / len(t | s) >= 0.5 for s in seen_tokens)

    fresh = [x for x in items if not repeated(x[key])]
    return (fresh + [x for x in items if x not in fresh])[:n]


def _lang_reminder(lang: str) -> str:
    return f"\n\nIMPORTANT: write everything except quotes in {LANG_NAMES[lang]}, whatever the language of the document."


def _attach(items: list, chunks: list[dict], lang: str) -> list:
    out = []
    for item in items[:MAX_ITEMS]:
        if isinstance(item, dict):
            item.update(_locate(item.get("quote", ""), chunks, lang))
            out.append(item)
    return out


async def _ask_json(prompt: str, doc: dict, text: str, max_tokens: int = 2500, temperature: float = 0.3,
                     lang: str | None = None) -> dict | None:
    if not settings.llm_enabled:
        return None
    content = f"Document: {doc['name']}\n\n{text}"
    if lang:  # напоминание в самом конце: иначе модель отвечает на языке документа
        content += "\n\n---" + _lang_reminder(lang)
    try:
        reply = await llm.complete(prompt, [{"role": "user", "content": content}],
                                   max_tokens=max_tokens, temperature=temperature)
    except llm.LLMError:
        return None
    return _parse_json(reply)


# ---------------------------------------------------------------- карта документа

INSIGHTS_PROMPT = """You are a document analyst. Build a detailed map of the WHOLE document.
Write every field (title, summary, event, label, text, term, definition) in {lang_name} — translate if the document
is in another language. Only "quote" stays in the document's original language.
Return ONLY valid JSON:
{{"title": "<short title of the document>",
  "summary": "<2-3 sentences: what this document is and why it matters>",
  "timeline": [{{"date": "<date or deadline>", "event": "<what happens>", "quote": "<exact phrase from the document>"}}],
  "numbers": [{{"value": "<number with unit, e.g. 3 people, 40 points, 24 months>", "label": "<what it means and which section / track / item it belongs to>", "quote": "<exact phrase>"}}],
  "requirements": [{{"text": "<one requirement / rule / obligation, short>", "quote": "<exact phrase>"}}],
  "terms": [{{"term": "<term, abbreviation or name>", "definition": "<short explanation>"}}]}}
Rules:
- Cover ALL sections of the document evenly (every chapter, track, direction, category), not only the first ones.
- "numbers": include EVERY significant number — scores and criteria weights, durations, ages, team sizes, counts,
  sizes and formats, money, percentages, limits. If the same kind of number exists for several sections or tracks,
  list it for EACH one. Up to 14 items.
- Up to 14 items in the other lists too, most important first; timeline sorted chronologically; empty list if nothing fits.
- Every "quote" MUST be copied word-for-word from the document in its ORIGINAL language (5-15 words)."""

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
    key = f"insights2:{lang}"  # v2: весь документ и все разделы (старые карты строились по половине текста)
    if doc.get("cache", {}).get(key):
        return doc["cache"][key]
    text, chunks = _doc_text(doc, MAP_BUDGET)
    data = await _ask_json(INSIGHTS_PROMPT.format(lang_name=LANG_NAMES[lang]), doc, text, max_tokens=5000, lang=lang)
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

QUIZ_PROMPT = """You create a knowledge test based ONLY on the document.
Write questions, options and explanations in {lang_name} — translate if the document is in another language.
Only "quote" stays in the document's original language.
Return ONLY valid JSON:
{{"questions": [{{"question": "<question>", "options": ["<A>", "<B>", "<C>", "<D>"], "answer": <index 0-3 of the correct option>,
  "explanation": "<1-2 sentences why it is correct>", "quote": "<exact phrase from the document proving the answer, original language>"}}]}}
Create exactly {n} questions about important facts, rules and numbers from DIFFERENT parts of the text.
Distractors must be plausible. Every question must be answerable from the document.
Variant #{seed} — make this set different from any previous one."""

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


def _shuffle_options(item: dict, rng: random.Random) -> dict:
    """Правильный ответ — на случайной позиции (модели любят ставить его вторым)."""
    order = list(range(len(item["options"])))
    rng.shuffle(order)
    item["options"] = [item["options"][i] for i in order]
    item["answer"] = order.index(item["answer"])
    return item


async def quiz(doc: dict, lang: str, n: int = 5) -> dict:
    _, chunks = _doc_text(doc)
    seen_key = f"quiz_seen:{lang}"
    seen = _seen(doc, seen_key)
    rng = random.Random()
    # уникальный запрос: разный фрагмент текста, номер варианта и список уже заданных вопросов
    # просим с запасом: похожие на прошлые вопросы отсеиваются
    prompt = QUIZ_PROMPT.format(lang_name=LANG_NAMES[lang], n=n + 3, seed=rng.randint(1000, 9999)) + _avoid(seen)
    # кириллица «дороже» в токенах: 10+3 вопросов с объяснениями не помещаются в 3000
    data = await _ask_json(prompt, doc, _random_text(chunks), max_tokens=700 * (n + 3), temperature=0.9, lang=lang)
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
        questions.append(_shuffle_options(item, rng))
    if questions:
        questions = _fresh_first(questions, "question", seen, n)
        _remember(doc, seen_key, [q["question"] for q in questions])
        return {"questions": questions}
    return {"questions": _offline_quiz(chunks, lang, n), "offline": True}


# ---------------------------------------------------------------- карточки для запоминания

CARDS_PROMPT = """You create flashcards for memorizing the document.
Write "front" and "back" in {lang_name} — translate if the document is in another language.
Only "quote" stays in the document's original language.
Return ONLY valid JSON:
{{"cards": [{{"front": "<short question or term, under 90 characters>",
  "back": "<the answer: short and exact, under 160 characters, with the precise number / date / name>",
  "quote": "<exact phrase from the document proving the answer, original language>"}}]}}
Create exactly {n} cards about key facts, numbers, deadlines, rules and terms from DIFFERENT parts of the text.
Variant #{seed}."""


def _offline_cards(chunks: list[dict], lang: str, n: int) -> list[dict]:
    cards = []
    for q in _offline_quiz(chunks, lang, n):
        cards.append({"front": q["question"], "back": q["options"][q["answer"]], "quote": q["quote"],
                      **{k: q[k] for k in ("chunk_id", "loc", "loc_label")}})
    return cards


async def cards(doc: dict, lang: str, n: int = 10) -> dict:
    _, chunks = _doc_text(doc)
    seen_key = f"cards_seen:{lang}"
    seed = random.randint(1000, 9999)
    seen = _seen(doc, seen_key)
    prompt = CARDS_PROMPT.format(lang_name=LANG_NAMES[lang], n=n + 3, seed=seed) + _avoid(seen)
    data = await _ask_json(prompt, doc, _random_text(chunks), max_tokens=300 * (n + 3), temperature=0.9, lang=lang)
    out = []
    for c in (data or {}).get("cards", []) if isinstance(data, dict) else []:
        if not isinstance(c, dict) or not c.get("front") or not c.get("back"):
            continue
        item = {"front": str(c["front"]), "back": str(c["back"]), "quote": str(c.get("quote", ""))}
        item.update(_locate(item["quote"], chunks, lang))
        out.append(item)
    if out:
        out = _fresh_first(out, "front", seen, n)
        _remember(doc, seen_key, [c["front"] for c in out])
        return {"cards": out}
    return {"cards": _offline_cards(chunks, lang, n), "offline": True}


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
