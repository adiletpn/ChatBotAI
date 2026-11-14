"""Сравнение двух версий документа: что добавили, удалили и изменили.

1. Оба файла заново разбираются на страницы, текст режется на предложения.
2. difflib сопоставляет последовательности предложений; изменённые предложения
   дополнительно сравниваются по словам — видно, что именно поменялось (24 → 36 месяцев).
3. LLM кратко объясняет смысл изменений: что важно и на что обратить внимание.
"""
from __future__ import annotations

import asyncio
import difflib
import json
import logging
import re
from collections import OrderedDict

import datetime as dt
import io

from . import llm
from .chunker import split_sentences
from .config import settings
from .lang import LANG_NAMES, format_loc
from .parsers import parse_file
from .store import store

log = logging.getLogger(__name__)

MAX_CHANGES = 300
_cache: OrderedDict[tuple, dict] = OrderedDict()  # (id_a, id_b, lang) -> результат

COMPARE_PROMPT = """You compare two versions of a document (OLD and NEW) given as a list of changes.
Respond in {lang_name}. Return ONLY valid JSON:
{{"verdict": "<one sentence: what kind of revision this is overall>",
  "points": ["<the most important change and what it means in practice>", "..."],
  "attention": ["<a change that may affect the reader's obligations, money, deadlines or rights>", "..."]}}
Up to 6 points and up to 3 attention items. Be specific: quote numbers, dates and names. Do not invent anything."""


# «3.2», «5.1.2», «7.» или «7)» в начале предложения; «100 балл» и «2026 жылғы» — не пункты
# после номера — текст пункта с заглавной буквы («1.8 метра» — это число, а не пункт)
CLAUSE_RE = re.compile(r"^(\d{1,2}(?:\.\d{1,2})+|\d{1,2}(?=[.)]))[.)]?(?:\s+(?=[A-ZА-ЯЁӘҒҚҢӨҰҮҺІ«\"])|$)")
CLAUSE_WORD = {"kk": "{}-тармақ", "ru": "п. {}", "en": "clause {}"}


def _sentences(doc: dict) -> list[tuple[str, dict, str]]:
    """Предложения документа: (текст, страница, номер пункта «3.2» — если документ нумерованный)."""
    pages = parse_file(doc["name"], store.file_path(doc).read_bytes())
    out, clause = [], ""
    for page in pages:
        text = re.sub(r"(\w)-\n(\w)", r"\1\2", page["text"])
        text = re.sub(r"[ \t]*\n[ \t]*", "\n", text)
        for sentence in split_sentences(text):
            sentence = re.sub(r"\s+", " ", sentence).strip().lstrip("#").strip()
            m = CLAUSE_RE.match(sentence)
            if m:
                clause = m.group(1)
                if not sentence[m.end():].strip():  # «3.2.» отдельным куском — это только номер пункта
                    continue
            if len(sentence) > 1:
                out.append((sentence, page["loc"], clause))
    return out


def _where(item: tuple, lang: str) -> str:
    """«стр. 2 · п. 3.2»; у Word-документов страниц нет — только номер пункта."""
    _, loc, clause = item
    page = format_loc(loc, lang) if loc.get("type") in ("page", "slide", "sheet") else ""
    parts = [page, CLAUSE_WORD[lang].format(clause) if clause else ""]
    return " · ".join(p for p in parts if p) or format_loc(loc, lang)


def _norm(sentence: str) -> str:
    return re.sub(r"[^\w]+", " ", sentence.lower().replace("ё", "е")).strip()


def _word_diff(old: str, new: str) -> list[list[str]]:
    """Пословное сравнение: [["eq"|"del"|"ins", текст], ...]."""
    a, b = re.findall(r"\S+|\s+", old), re.findall(r"\S+|\s+", new)
    parts: list[list[str]] = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            parts.append(["eq", "".join(a[i1:i2])])
            continue
        if i2 > i1:
            parts.append(["del", "".join(a[i1:i2])])
        if j2 > j1:
            parts.append(["ins", "".join(b[j1:j2])])
    return parts


def diff_docs(doc_a: dict, doc_b: dict, lang: str) -> dict:
    """Чистое сравнение без LLM (выполняется в потоке)."""
    old, new = _sentences(doc_a), _sentences(doc_b)
    matcher = difflib.SequenceMatcher(None, [_norm(s[0]) for s in old], [_norm(s[0]) for s in new], autojunk=False)
    changes, stats = [], {"added": 0, "removed": 0, "changed": 0}
    loc = lambda item: _where(item, lang)  # noqa: E731

    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            continue
        olds, news = old[i1:i2], new[j1:j2]
        if op == "replace":
            # равное число предложений — сравниваем попарно, иначе блоком
            pairs = list(zip(olds, news)) if len(olds) == len(news) else [(
                (" ".join(s[0] for s in olds), *olds[0][1:]), (" ".join(s[0] for s in news), *news[0][1:]))]
            for o, n in pairs:
                stats["changed"] += 1
                changes.append({"kind": "changed", "old": o[0], "new": n[0], "loc_old": loc(o), "loc_new": loc(n),
                                "words": _word_diff(o[0], n[0])})
        elif op == "delete":
            stats["removed"] += 1
            changes.append({"kind": "removed", "old": " ".join(s[0] for s in olds), "loc_old": loc(olds[0])})
        else:
            stats["added"] += 1
            changes.append({"kind": "added", "new": " ".join(s[0] for s in news), "loc_new": loc(news[0])})

    stats["similarity"] = round(matcher.ratio() * 100)
    stats["total"] = len(changes)
    return {"stats": stats, "changes": changes[:MAX_CHANGES], "truncated": len(changes) > MAX_CHANGES}


def _changes_text(changes: list[dict], budget: int = 12000) -> str:
    lines = []
    for c in changes:
        if c["kind"] == "changed":
            lines.append(f"CHANGED ({c['loc_new']}): \"{c['old']}\" → \"{c['new']}\"")
        elif c["kind"] == "removed":
            lines.append(f"REMOVED ({c['loc_old']}): \"{c['old']}\"")
        else:
            lines.append(f"ADDED ({c['loc_new']}): \"{c['new']}\"")
    return "\n".join(lines)[:budget]


DIFFERENT_AT = 50  # совпадение текста ниже этого (%) — это не версии, а разные документы

DIFFERENT_PROMPT = """You compare two DIFFERENT documents (A and B) for a reader who must understand how they differ.
Respond in {lang_name}. Return ONLY valid JSON:
{{"verdict": "<one or two sentences: what each document is and the main difference>",
  "rows": [{{"aspect": "<aspect>", "a": "<what A says, short, with exact numbers/dates>", "b": "<what B says>"}}],
  "common": ["<what both documents share>"],
  "only_a": ["<important thing present only in A>"],
  "only_b": ["<important thing present only in B>"]}}
Rows: 5-9 aspects that matter for these documents (e.g. purpose/topic, deadlines, participants, requirements,
evaluation, money, format, contacts). Write "—" if a document says nothing about an aspect.
Up to 5 items in each list. Use only facts from the texts; do not invent anything.
Write EVERY cell and item in {lang_name}, translating from the documents' language; keep numbers and names exact.
In the verdict refer to the documents by their file names, never as "A" and "B"."""


def _doc_text(doc: dict, budget: int = 9000) -> str:
    """Начало и равномерная выборка фрагментов — чтобы модель видела весь документ, а не только первую страницу."""
    chunks = store.doc_chunks({doc["id"]})
    text = "\n".join(c["text"] for c in chunks)
    if len(text) <= budget:
        return text
    step = max(1, len(chunks) * 900 // budget + 1)
    return "\n".join(c["text"] for c in chunks[::step])[:budget]


async def _different(doc_a: dict, doc_b: dict, lang: str) -> dict | None:
    if not settings.llm_enabled:
        return None
    try:
        reply = await llm.complete(
            DIFFERENT_PROMPT.format(lang_name=LANG_NAMES[lang]),
            [{"role": "user", "content": f"DOCUMENT A: {doc_a['name']}\n{_doc_text(doc_a)}\n\n"
                                         f"DOCUMENT B: {doc_b['name']}\n{_doc_text(doc_b)}"}],
            max_tokens=2500,
        )
        start, end = reply.find("{"), reply.rfind("}")
        data = json.loads(reply[start:end + 1]) if start != -1 and end > start else None
    except (llm.LLMError, json.JSONDecodeError) as exc:
        log.warning("Сравнение разных документов не удалось: %s", exc)
        return None
    if not data or not data.get("rows"):
        return None
    rows = [{"aspect": str(r.get("aspect", "")), "a": str(r.get("a", "—")), "b": str(r.get("b", "—"))}
            for r in data["rows"] if isinstance(r, dict)][:10]
    lists = {k: [str(x) for x in data.get(k, [])][:5] for k in ("common", "only_a", "only_b")}
    return {"verdict": str(data.get("verdict", "")), "rows": rows, **lists}


async def compare(doc_a: dict, doc_b: dict, lang: str) -> dict:
    key = (doc_a["id"], doc_b["id"], lang)
    if key in _cache:
        return _cache[key]
    result = await asyncio.to_thread(diff_docs, doc_a, doc_b, lang)
    result["a"] = {"id": doc_a["id"], "name": doc_a["name"]}
    result["b"] = {"id": doc_b["id"], "name": doc_b["name"]}
    result["summary"] = None
    if result["stats"]["similarity"] < DIFFERENT_AT:
        # разные документы: пословная разница бессмысленна — сравниваем по смыслу, таблицей
        result["kind"] = "different"
        result["changes"] = []
        result["table"] = await _different(doc_a, doc_b, lang)
        if result["table"] or not settings.llm_enabled:
            _cache[key] = result
        return result
    result["kind"] = "versions"
    if result["changes"] and settings.llm_enabled:
        try:
            reply = await llm.complete(
                COMPARE_PROMPT.format(lang_name=LANG_NAMES[lang]),
                [{"role": "user", "content": f"OLD: {doc_a['name']}\nNEW: {doc_b['name']}\n\nCHANGES:\n"
                                             + _changes_text(result["changes"])}],
                max_tokens=1200,
            )
            start, end = reply.find("{"), reply.rfind("}")
            data = json.loads(reply[start:end + 1]) if start != -1 and end > start else None
            if data and data.get("verdict"):
                result["summary"] = {
                    "verdict": str(data["verdict"]),
                    "points": [str(p) for p in data.get("points", [])][:6],
                    "attention": [str(p) for p in data.get("attention", [])][:3],
                }
        except (llm.LLMError, json.JSONDecodeError) as exc:
            log.warning("Сводка сравнения не удалась: %s", exc)
    if result["summary"] or not (result["changes"] and settings.llm_enabled):  # неудачную сводку не кэшируем
        _cache[key] = result
    while len(_cache) > 50:
        _cache.popitem(last=False)
    return result


# ---------------------------------------------------------------- проверка на подделку
#
# По тексту видно, ЧТО изменили; по служебным данным файла — признаки правки: когда файл создан и изменён,
# в какой программе, сколько раз пересохранялся. Это признаки, а не доказательство подделки.

EDITORS = ("ilovepdf", "smallpdf", "sejda", "pdfescape", "pdf24", "foxit", "nitro", "pdfelement", "wondershare",
           "pdf-xchange", "pdffiller", "docfly", "pdfcandy", "sodapdf", "pdf2go", "online2pdf")
RISKY = re.compile(r"\d|₸|\$|€|тг|тенге|теңге|руб|сом|usd|kzt|%", re.I)

SIGNALS = {
    "edited_after": {"kk": "Жасалғаннан кейін өзгертілген: {a} → {b}", "ru": "Изменён после создания: {a} → {b}",
                     "en": "Modified after creation: {a} → {b}"},
    "resaved": {"kk": "Файл {n} рет қайта сақталған (PDF-қа түзетулер қосылған)", "ru": "Файл пересохранялся {n} раз(а) — в PDF дописаны правки",
                "en": "File was re-saved {n} times — edits appended to the PDF"},
    "editor": {"kk": "PDF-редакторда өңделген: {x}", "ru": "Обработан в PDF-редакторе: {x}", "en": "Processed in a PDF editor: {x}"},
    "other_author": {"kk": "Соңғы өзгерткен: {x} (авторы: {y})", "ru": "Последним изменял: {x} (автор: {y})",
                     "en": "Last modified by {x} (author: {y})"},
    "earlier": {"kk": "Екінші файлдан ертерек жасалған", "ru": "Создан раньше второго файла", "en": "Created earlier than the other file"},
    "clean": {"kk": "Түзету белгілері жоқ", "ru": "Признаков правки не найдено", "en": "No signs of editing found"},
}


def _sig(key: str, lang: str, **kw) -> str:
    return SIGNALS[key][lang].format(**kw)


def _pdf_date(value: str) -> dt.datetime | None:
    m = re.match(r"D:(\d{4})(\d{2})(\d{2})(\d{2})?(\d{2})?(\d{2})?", value or "")
    if not m:
        return None
    parts = [int(x) if x else 0 for x in m.groups()]
    try:
        return dt.datetime(*parts)
    except ValueError:
        return None


def _fmt(d: dt.datetime | None) -> str:
    return d.strftime("%d.%m.%Y %H:%M") if d else "—"


def file_traces(doc: dict, lang: str) -> dict:
    """Служебные данные файла и признаки правки. score — чем больше, тем вероятнее файл правили."""
    data = store.file_path(doc).read_bytes()
    info = {"created": None, "modified": None, "program": "", "resaves": 0}
    signals, score = [], 0
    if doc["ext"] == ".pdf":
        import pymupdf

        with pymupdf.open(stream=data, filetype="pdf") as pdf:
            meta = pdf.metadata or {}
        info["created"], info["modified"] = _pdf_date(meta.get("creationDate", "")), _pdf_date(meta.get("modDate", ""))
        info["program"] = " / ".join(x for x in (meta.get("creator", ""), meta.get("producer", "")) if x)
        info["resaves"] = max(0, data.count(b"%%EOF") - 1)  # каждое «дописанное» сохранение PDF добавляет %%EOF
        if info["resaves"]:
            signals.append(_sig("resaved", lang, n=info["resaves"]))
            score += 2
        editor = next((e for e in EDITORS if e in info["program"].lower()), None)
        if editor:
            signals.append(_sig("editor", lang, x=info["program"][:60]))
            score += 2
    elif doc["ext"] == ".docx":
        import docx

        core = docx.Document(io.BytesIO(data)).core_properties
        info["created"], info["modified"] = core.created, core.modified
        info["program"] = f"Word · ред. {core.revision}" if core.revision else "Word"
        if core.last_modified_by and core.author and core.last_modified_by != core.author:
            signals.append(_sig("other_author", lang, x=core.last_modified_by, y=core.author))
            score += 1
    created, modified = info["created"], info["modified"]
    if created and modified:
        created, modified = created.replace(tzinfo=None), modified.replace(tzinfo=None)
        if (modified - created).total_seconds() > 120:
            signals.insert(0, _sig("edited_after", lang, a=_fmt(created), b=_fmt(modified)))
            score += 2
    return {"id": doc["id"], "name": doc["name"], "created": _fmt(created), "modified": _fmt(modified),
            "program": info["program"] or "—", "signals": signals, "score": score, "_created": created}


def _risk(change: dict) -> str:
    """Изменения сумм, дат, номеров и процентов — самые опасные при подделке."""
    if change["kind"] == "changed":
        edited = " ".join(t for op, t in change["words"] if op != "eq")
    else:
        edited = change.get("new") or change.get("old") or ""
    return "high" if RISKY.search(edited) else "medium"


FORGERY_PROMPT = """You check whether a document was falsified. ORIGINAL is the trusted file, CHECKED may be forged.
Respond in {lang_name}. Return ONLY valid JSON:
{{"verdict": "<one sentence: does CHECKED match ORIGINAL, and how serious are the differences>",
  "suspicious": ["<a change that looks like falsification: amounts, dates, names, numbers, obligations — quote old → new>", "..."]}}
Up to 6 suspicious items, most dangerous first. Be specific and do not invent anything.
Refer to the files by their names (never write "ORIGINAL" or "CHECKED")."""


async def forgery(original: dict, checked: dict, lang: str) -> dict:
    """Проверка подлинности: что изменено в проверяемом файле и какой файл больше похож на оригинал."""
    key = (original["id"], checked["id"], lang, "forgery")
    if key in _cache:
        return _cache[key]
    result = await asyncio.to_thread(diff_docs, original, checked, lang)
    for change in result["changes"]:
        change["risk"] = _risk(change)
    result["changes"].sort(key=lambda c: c["risk"] != "high")  # опасные — первыми
    result["stats"]["risky"] = sum(c["risk"] == "high" for c in result["changes"])
    result["a"] = {"id": original["id"], "name": original["name"]}
    result["b"] = {"id": checked["id"], "name": checked["name"]}
    result["mode"] = "forgery"

    traces = await asyncio.to_thread(lambda: [file_traces(original, lang), file_traces(checked, lang)])
    ca, cb = traces[0].pop("_created"), traces[1].pop("_created")
    if ca and cb and ca != cb:
        earlier = traces[0] if ca < cb else traces[1]
        earlier["signals"].append(_sig("earlier", lang))
        earlier["score"] -= 1
    for tr in traces:
        if not tr["signals"]:
            tr["signals"].append(_sig("clean", lang))
    # какой файл похож на оригинал: меньше признаков правки; при равенстве — не угадываем
    diff = traces[0]["score"] - traces[1]["score"]
    result["traces"] = traces
    result["likely_original"] = None if diff == 0 else ("a" if diff < 0 else "b")

    result["summary"] = None
    if result["changes"] and settings.llm_enabled:
        try:
            reply = await llm.complete(
                FORGERY_PROMPT.format(lang_name=LANG_NAMES[lang]),
                [{"role": "user", "content": f"ORIGINAL: {original['name']}\nCHECKED: {checked['name']}\n\nCHANGES:\n"
                                             + _changes_text(result["changes"])}],
                max_tokens=1200,
            )
            start, end = reply.find("{"), reply.rfind("}")
            data = json.loads(reply[start:end + 1]) if start != -1 and end > start else None
            if data and data.get("verdict"):
                result["summary"] = {"verdict": str(data["verdict"]), "points": [],
                                     "attention": [str(p) for p in data.get("suspicious", [])][:6]}
        except (llm.LLMError, json.JSONDecodeError) as exc:
            log.warning("Сводка проверки не удалась: %s", exc)
    if result["summary"] or not (result["changes"] and settings.llm_enabled):
        _cache[key] = result
    return result
