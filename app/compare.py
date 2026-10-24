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


async def compare(doc_a: dict, doc_b: dict, lang: str) -> dict:
    key = (doc_a["id"], doc_b["id"], lang)
    if key in _cache:
        return _cache[key]
    result = await asyncio.to_thread(diff_docs, doc_a, doc_b, lang)
    result["a"] = {"id": doc_a["id"], "name": doc_a["name"]}
    result["b"] = {"id": doc_b["id"], "name": doc_b["name"]}
    result["summary"] = None
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
