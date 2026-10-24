"""RAG (Retrieval-Augmented Generation) — ядро чат-бота.

Схема ответа на вопрос:
  1. определяем язык вопроса (kk / ru / en);
  2. LLM переводит запрос на три языка — так находим ответ, даже если документ на другом языке;
  3. гибридный поиск: BM25 (совпадение слов) + эмбеддинги (совпадение смысла), результаты
     объединяются методом RRF; короткие документы модель получает целиком;
  4. LLM формирует ответ строго по фрагментам и ставит ссылки [1], [2] на источники;
     в режиме Mind Pro модель со «зрением» дополнительно видит сами страницы PDF —
     таблицы, графики и схемы, которые теряются при извлечении текста;
  5. без LLM работает офлайн-режим — извлекаются самые подходящие предложения.
"""
import asyncio
import json
import logging
import math
import re
from collections import OrderedDict
from pathlib import Path
from typing import AsyncIterator

from . import llm
from .chunker import chunk_pages, split_sentences
from .config import settings
from .lang import LANG_NAMES, detect_lang, format_loc, t
from .parsers import IMAGE_EXT, parse_file
from .retriever import tokenize
from .semantic import semantic
from .store import store

log = logging.getLogger(__name__)


# ---------------------------------------------------------------- загрузка

def ingest(owner: str, filename: str, data: bytes) -> dict:
    """Разбирает файл, режет на фрагменты, индексирует. Выполняется в отдельном потоке."""
    pages = parse_file(filename, data)
    if not pages:
        raise ValueError("В документе не найден текст (возможно, это скан, а OCR недоступен)")
    doc_id = store.new_id()
    ext = Path(filename).suffix.lower()
    store.file_path({"id": doc_id, "ext": ext}).write_bytes(data)
    chunks = chunk_pages(doc_id, pages, settings.chunk_size, settings.chunk_overlap)
    return store.add(doc_id, owner, Path(filename).name, ext, len(data), pages, chunks)


# ---------------------------------------------------------------- история диалога

class History:
    def __init__(self, max_sessions: int = 1000):
        self.max_sessions = max_sessions
        self.sessions: OrderedDict[str, list[dict]] = OrderedDict()

    def get(self, key: str) -> list[dict]:
        if key in self.sessions:
            self.sessions.move_to_end(key)
        return self.sessions.get(key, [])

    def add(self, key: str, question: str, answer: str) -> None:
        turns = self.sessions.setdefault(key, [])
        turns += [{"role": "user", "content": question}, {"role": "assistant", "content": answer}]
        del turns[:-settings.history_turns * 2]
        self.sessions.move_to_end(key)
        while len(self.sessions) > self.max_sessions:
            self.sessions.popitem(last=False)

    def clear(self, key: str) -> None:
        self.sessions.pop(key, None)


history = History()


# ---------------------------------------------------------------- промпты

SYSTEM_PROMPT = """You are Mind AI — an intelligent assistant that answers questions strictly based on the user's uploaded documents (PDF, DOCX and others).

Rules:
1. Use ONLY the information from the numbered CONTEXT fragments. Never invent facts, numbers, dates or names.
2. If the context does not contain the answer, say honestly: "{not_found}" — and briefly suggest what the documents do cover.
   If the question is unclear, too short or meaningless, do NOT summarize the documents: in ONE short sentence ask
   the user to clarify, and cite nothing.
3. Answer in {lang_name} — the language of the user's question — even if the documents are written in another language. Translate faithfully, keep names, numbers and dates exact.
4. Cite sources: after every statement put the fragment number in square brackets, e.g. [1] or [2][4]. Cite only fragments you actually used.
5. Start with the direct answer, then add details. Use short paragraphs, bullet lists or markdown tables when it improves clarity. Be precise and easy to understand.
6. If the question is about the whole document (summary, structure, main points), synthesize from all fragments."""

EXPAND_PROMPT = """You help a search engine. Rewrite the user's question as search keywords in THREE languages.
Return exactly three lines, no explanations:
kk: <keywords in Kazakh>
ru: <keywords in Russian>
en: <keywords in English>
Include synonyms and important terms (names, numbers) from the question."""

SUMMARY_PROMPT = """You analyze a document. Respond in {lang_name}, even if the document is in another language.
Return ONLY valid JSON of the form:
{{"summary": "<3-5 sentences: what the document is, its purpose and key points>",
  "questions": ["<question 1>", "<question 2>", "<question 3>", "<question 4>"]}}
The questions must be useful, specific questions a reader might ask that the document answers."""


# ---------------------------------------------------------------- поиск контекста

async def _expand_query(question: str) -> str:
    if not (settings.llm_enabled and settings.query_expansion):
        return ""
    try:
        text = await asyncio.wait_for(
            llm.complete(EXPAND_PROMPT, [{"role": "user", "content": question}], max_tokens=200, temperature=0),
            timeout=25,
        )
        return re.sub(r"^(kk|ru|en)\s*:\s*", "", text, flags=re.M)
    except (llm.LLMError, asyncio.TimeoutError) as exc:
        log.warning("Расширение запроса не удалось: %s", exc)
        return ""


RRF_K = 60  # константа Reciprocal Rank Fusion: важен ранг в каждом списке, а не «сырые» баллы


def _search(queries: list[str], doc_ids: set[str], top_k: int) -> list[tuple[dict, float]]:
    """Гибридный поиск: BM25 по словам + эмбеддинги по смыслу, оба по всем вариантам запроса
    (оригинал + переводы). Списки объединяются по RRF: фрагмент, найденный обоими способами, — выше."""
    best: dict[str, tuple[dict, float]] = {}
    for query in queries:
        if not query.strip():
            continue
        for chunk, score in store.index.search(query, top_k=top_k * 2, allowed_docs=doc_ids):
            if chunk["id"] not in best or best[chunk["id"]][1] < score:
                best[chunk["id"]] = (chunk, score)
    keyword = sorted(best.values(), key=lambda item: item[1], reverse=True)[:top_k * 2]
    meaning = semantic.search(queries, store.doc_chunks(doc_ids), top_k * 2)

    fused: dict[str, tuple[dict, float]] = {}
    for ranked in (keyword, meaning):
        for rank, (chunk, _) in enumerate(ranked):
            prev = fused.get(chunk["id"], (chunk, 0.0))[1]
            fused[chunk["id"]] = (chunk, prev + 1 / (RRF_K + rank + 1))
    return sorted(fused.values(), key=lambda item: item[1], reverse=True)[:top_k]


def _with_neighbors(hits: list[tuple[dict, float]], all_chunks: list[dict], limit: int) -> list[dict]:
    """Добавляет соседние фрагменты к двум лучшим — ответ часто продолжается в следующем абзаце."""
    by_key = {(c["doc_id"], c["idx"]): c for c in all_chunks}
    selected: dict[str, dict] = {c["id"]: c for c, _ in hits}
    for chunk, _ in hits[:2]:
        for delta in (-1, 1):
            neighbor = by_key.get((chunk["doc_id"], chunk["idx"] + delta))
            if neighbor and len(selected) < limit:
                selected.setdefault(neighbor["id"], neighbor)
    return list(selected.values())


def _order(chunks: list[dict], doc_order: list[str]) -> list[dict]:
    rank = {doc_id: i for i, doc_id in enumerate(doc_order)}
    return sorted(chunks, key=lambda c: (rank.get(c["doc_id"], 0), c["idx"]))


def _source(n: int, chunk: dict, score: float, lang: str) -> dict:
    doc = store.get(chunk["doc_id"]) or {}
    return {
        "n": n,
        "chunk_id": chunk["id"],
        "doc_id": chunk["doc_id"],
        "doc_name": doc.get("name", "?"),
        "loc": chunk["loc"],
        "loc_label": format_loc(chunk["loc"], lang),
        "text": chunk["text"],
        "score": round(score, 3),
    }


# ---------------------------------------------------------------- офлайн-ответ

def _extractive_answer(query: str, sources: list[dict], ranked_ns: list[int], lang: str) -> tuple[str, list[int]]:
    q_terms = set(tokenize(query))
    by_n = {s["n"]: s for s in sources}
    scored, seen = [], set()
    for rank, n in enumerate(ranked_ns[:5]):
        for pos, sentence in enumerate(split_sentences(by_n[n]["text"])):
            tokens = tokenize(sentence)
            if len(tokens) < 3 or sentence in seen:  # соседние фрагменты перекрываются
                continue
            seen.add(sentence)
            overlap = len(q_terms & set(tokens))
            if overlap:
                score = overlap / math.sqrt(len(tokens)) - rank * 0.05
                scored.append((score, n, pos, sentence))
    if not scored:
        return t("not_found", lang), []
    top = sorted(scored, reverse=True)[:4]
    top.sort(key=lambda item: (ranked_ns.index(item[1]), item[2]))
    lines = [f"- {sentence} [{n}]" for _, n, _, sentence in top]
    cited = sorted({n for _, n, _, _ in top})
    return "\n".join(lines) + "\n\n" + t("offline_note", lang), cited


# ---------------------------------------------------------------- ответ

def _cited(answer: str, valid: set[int]) -> list[int]:
    found = []
    for m in re.findall(r"\[(\d+(?:\s*[,;]\s*\d+)*)\]", answer):
        for part in re.split(r"[,;]", m):
            n = int(part)
            if n in valid and n not in found:
                found.append(n)
    return found


STYLE_RULES = {
    "concise": "Keep the answer short: 1-3 sentences, or a very short list if essential.",
    "balanced": "",
    "detailed": "Give a thorough, well-structured answer that covers every relevant detail from the context.",
}


async def answer_stream(question: str, owner: str, session_key: str,
                        doc_ids: list[str] | None = None, prefs: dict | None = None) -> AsyncIterator[dict]:
    """Генератор событий: {"type": "sources"|"delta"|"done"|"error", ...}
    prefs — настройки пользователя: answer_style (concise|balanced|detailed), answer_model (lite|pro).
    Язык ответа — всегда язык вопроса."""
    prefs = prefs or {}
    question = question.strip()
    lang = detect_lang(question)
    docs = store.list(owner)
    if doc_ids:
        docs = [d for d in docs if d["id"] in set(doc_ids)] or docs
    if not docs:
        yield {"type": "delta", "text": t("no_docs", lang)}
        yield {"type": "done", "cited": [], "lang": lang}
        return

    allowed = {d["id"] for d in docs}
    all_chunks = store.doc_chunks(allowed)
    past = history.get(session_key)

    yield {"type": "status", "step": "search"}  # «ход мыслей» в интерфейсе: что бот делает прямо сейчас
    # Короткий уточняющий вопрос («а сколько баллов?») ищем вместе с предыдущим вопросом
    search_query = question
    if past and len(tokenize(question)) <= 2:
        search_query = past[-2]["content"] + " " + question
    expanded = await _expand_query(search_query)
    pro = prefs.get("answer_model") == "pro" and settings.llm_enabled
    top_k = settings.top_k * 2 if pro else settings.top_k  # Mind Pro читает вдвое больше фрагментов
    # каждый перевод — отдельный запрос: эмбеддинг смешанной строки на трёх языках теряет смысл
    hits = _search([search_query, *expanded.splitlines()], allowed, top_k)
    total_chars = sum(d["chars"] for d in docs)

    if total_chars <= settings.full_context_chars:
        context = all_chunks  # документ небольшой — модель видит его целиком
    elif hits:
        context = _with_neighbors(hits, all_chunks, top_k + 3)
    else:
        context = all_chunks[:top_k]  # ничего не нашли — даём начало документов
    context = _order(context, [d["id"] for d in docs])

    scores = {c["id"]: s for c, s in hits}
    sources = [_source(i, chunk, scores.get(chunk["id"], 0.0), lang) for i, chunk in enumerate(context, start=1)]
    n_by_id = {chunk["id"]: i for i, chunk in enumerate(context, start=1)}
    ranked_ns = [n_by_id[c["id"]] for c, _ in hits if c["id"] in n_by_id]
    yield {"type": "sources", "sources": sources, "lang": lang}

    if not settings.llm_enabled:
        text, cited = _extractive_answer(search_query + " " + expanded, sources, ranked_ns, lang)
        yield {"type": "delta", "text": text}
        history.add(session_key, question, text)
        yield {"type": "done", "cited": cited, "lang": lang}
        return

    context_text = "\n\n".join(
        f"[{s['n']}] ({s['doc_name']}{', ' + s['loc_label'] if s['loc_label'] else ''})\n{s['text']}" for s in sources
    )
    system = SYSTEM_PROMPT.format(lang_name=LANG_NAMES[lang], not_found=t("not_found", lang))
    if STYLE_RULES.get(prefs.get("answer_style", "")):
        system += "\n7. " + STYLE_RULES[prefs["answer_style"]]
    user_message = f"CONTEXT:\n{context_text}\n\nQUESTION: {question}"
    messages = [*past, {"role": "user", "content": user_message}]

    parts: list[str] = []
    yield {"type": "status", "step": "write"}
    if pro:
        pages = await asyncio.to_thread(_page_images, [c for c, _ in hits] + context, sources, lang)
        if pages:
            yield {"type": "vision", "pages": [p["info"] for p in pages]}
            content = [{"type": "text", "text": user_message}]
            for page in pages:
                content += [{"type": "text", "text": page["label"]}, llm.image_part(page["data"], "image/jpeg")]
            try:
                async for delta in llm.stream_chat(system + VISION_RULE, [*past, {"role": "user", "content": content}],
                                                   model=settings.vision_model):
                    parts.append(delta)
                    yield {"type": "delta", "text": delta}
            except llm.LLMError as exc:  # модель со зрением недоступна — отвечаем обычной по тексту
                log.warning("Mind Pro (зрение) не ответила: %s", exc)
                if parts:
                    yield {"type": "error", "message": str(exc)[:300]}

    try:
        if not parts:
            async for delta in llm.stream_chat(system, messages):
                parts.append(delta)
                yield {"type": "delta", "text": delta}
    except llm.LLMError as exc:
        log.error("Ошибка LLM: %s", exc)
        if not parts:
            text, cited = _extractive_answer(search_query + " " + expanded, sources, ranked_ns, lang)
            note = t("llm_error", lang)
            text = text.replace("\n\n" + t("offline_note", lang), "")  # одна пометка вместо двух
            yield {"type": "delta", "text": f"⚠️ {note}\n\n{text}"}
            yield {"type": "done", "cited": cited, "lang": lang, "error": str(exc)[:300]}
            return
        yield {"type": "error", "message": str(exc)[:300]}

    answer = "".join(parts).strip()
    history.add(session_key, question, answer)
    # модель не сослалась ни на что (приветствие, «уточните вопрос») — значит, и подтверждения нет
    cited = _cited(answer, {s["n"] for s in sources})
    yield {"type": "done", "cited": cited, "lang": lang}
    if prefs.get("suggestions", True) and answer:
        items = await _followups(question, answer, context_text, lang)
        if items:
            yield {"type": "followups", "items": items}


# ---------------------------------------------------------------- подсказки следующего вопроса

FOLLOWUP_PROMPT = """Suggest 3 short follow-up questions the user may want to ask next, in {lang_name}.
They must continue the conversation naturally and be answerable from the CONTEXT (do not repeat the question).
Each under 70 characters. Return ONLY a JSON array of 3 strings."""


async def _followups(question: str, answer: str, context_text: str, lang: str) -> list[str]:
    try:
        reply = await asyncio.wait_for(llm.complete(
            FOLLOWUP_PROMPT.format(lang_name=LANG_NAMES[lang]),
            [{"role": "user", "content": f"CONTEXT:\n{context_text[:6000]}\n\nQUESTION: {question}\n\nANSWER: {answer[:2000]}"}],
            max_tokens=300, temperature=0.5), timeout=25)
        start, end = reply.find("["), reply.rfind("]")
        items = json.loads(reply[start:end + 1]) if start != -1 and end > start else []
    except (llm.LLMError, asyncio.TimeoutError, json.JSONDecodeError) as exc:
        log.warning("Подсказки не удались: %s", exc)
        return []
    out = []
    for item in items:
        text = str(item).strip().strip('"')
        if 5 < len(text) <= 120 and text.lower() != question.lower() and text not in out:
            out.append(text)
    return out[:3]


# ---------------------------------------------------------------- Mind Pro: страницы как изображения

VISION_RULE = """
8. You also receive IMAGES of the most relevant document pages. Use them to read tables, charts, diagrams,
stamps and layout precisely — the extracted text may have lost this structure. When you use a page image,
cite the fragment numbers listed in its label."""


def _page_images(ranked: list[dict], sources: list[dict], lang: str) -> list[dict]:
    """Рендерит до PRO_PAGES страниц PDF (и загруженные фото), на которых лежат лучшие фрагменты."""
    import pymupdf

    ns_by_page: dict[tuple, list[int]] = {}
    for s in sources:
        ns_by_page.setdefault((s["doc_id"], s["loc"].get("type"), s["loc"].get("value")), []).append(s["n"])
    picked, out = [], []
    for chunk in ranked:
        key = (chunk["doc_id"], chunk["loc"].get("type"), chunk["loc"].get("value"))
        doc = store.get(chunk["doc_id"])
        visual = doc and ((doc["ext"] == ".pdf" and key[1] == "page") or (doc["ext"] in IMAGE_EXT and key[1] == "image"))
        if visual and key not in picked:
            picked.append(key)
        if len(picked) >= settings.pro_pages:
            break
    for doc_id, kind, value in picked:
        doc = store.get(doc_id)
        try:
            if kind == "page":
                with pymupdf.open(store.file_path(doc)) as pdf:
                    data = pdf[int(value) - 1].get_pixmap(dpi=130).tobytes("jpeg", jpg_quality=82)
            else:
                from PIL import Image
                import io

                img = Image.open(store.file_path(doc)).convert("RGB")
                img.thumbnail((1600, 1600))
                buf = io.BytesIO()
                img.save(buf, "JPEG", quality=85)
                data = buf.getvalue()
        except Exception as exc:  # noqa: BLE001 — страницу не удалось отрисовать, обходимся текстом
            log.warning("Не удалось отрисовать %s %s: %s", doc["name"], value, exc)
            continue
        ns = ns_by_page.get((doc_id, kind, value), [])
        refs = "".join(f"[{n}]" for n in ns)
        loc = {"type": kind, "value": value}
        out.append({
            "data": data,
            "label": f"PAGE IMAGE — {doc['name']}, {format_loc(loc, 'en')}" + (f" (fragments {refs})" if refs else ""),
            "info": {"doc_id": doc_id, "doc_name": doc["name"], "loc": loc, "loc_label": format_loc(loc, lang)},
        })
    return out


async def answer(question: str, owner: str, session_key: str, doc_ids: list[str] | None = None) -> dict:
    """Не потоковый вариант (для Telegram): собирает полный ответ."""
    text, sources, cited, lang = [], [], [], "ru"
    async for event in answer_stream(question, owner, session_key, doc_ids, {"suggestions": False}):
        if event["type"] == "sources":
            sources = event["sources"]
        elif event["type"] == "delta":
            text.append(event["text"])
        elif event["type"] == "done":
            cited, lang = event["cited"], event["lang"]
    by_n = {s["n"]: s for s in sources}
    return {"text": "".join(text).strip(), "sources": [by_n[n] for n in cited if n in by_n], "lang": lang}


# ---------------------------------------------------------------- резюме документа

FALLBACK_QUESTIONS = {
    "kk": ["Бұл құжат не туралы?", "Құжаттағы негізгі талаптар қандай?", "Қандай мерзімдер көрсетілген?"],
    "ru": ["О чём этот документ?", "Какие основные требования указаны?", "Какие сроки упоминаются?"],
    "en": ["What is this document about?", "What are the main requirements?", "What deadlines are mentioned?"],
}


def _parse_json(text: str) -> dict | None:
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        return None
    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return None


async def summarize(doc: dict, lang: str) -> dict:
    if doc["summary"].get(lang):
        return doc["summary"][lang]
    chunks = store.doc_chunks({doc["id"]})
    # Длинный документ: берём равномерную выборку фрагментов по всему тексту
    budget, picked = 12000, chunks
    if sum(len(c["text"]) for c in chunks) > budget:
        step = max(1, math.ceil(len(chunks) / (budget // settings.chunk_size)))
        picked = chunks[::step]
    text = "\n\n".join(c["text"] for c in picked)[:budget]

    result = None
    if settings.llm_enabled:
        try:
            reply = await llm.complete(
                SUMMARY_PROMPT.format(lang_name=LANG_NAMES[lang]),
                [{"role": "user", "content": f"Document: {doc['name']}\n\n{text}"}],
                max_tokens=800,
            )
            result = _parse_json(reply)
        except llm.LLMError as exc:
            log.warning("Резюме не удалось: %s", exc)
    if not result or not result.get("summary"):
        sentences = [s for s in split_sentences(text) if len(s) > 30][:3]
        return {"summary": " ".join(sentences), "questions": FALLBACK_QUESTIONS[lang], "offline": True}
    result = {"summary": str(result["summary"]), "questions": [str(q) for q in result.get("questions", [])][:5]}
    store.set_summary(doc["id"], lang, result)
    return result
