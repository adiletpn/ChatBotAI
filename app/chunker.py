"""Разбиение текста на фрагменты (chunks) с перекрытием — по границам абзацев и предложений."""
import re

_SENTENCE_END = re.compile(r"(?<=[.!?…;])\s+|\n+")


def _clean(text: str) -> str:
    text = text.replace("­", "")  # мягкие переносы
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)  # переносы слов в PDF
    text = re.sub(r"[ \t ]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in _SENTENCE_END.split(text) if s and s.strip()]


def _pieces(text: str) -> list[str]:
    """Предложения; у последнего предложения строки сохраняется перевод строки (важно для таблиц и списков)."""
    pieces = []
    for line in text.split("\n"):
        sentences = split_sentences(line)
        if sentences:
            sentences[-1] += "\n"
            pieces.extend(sentences)
    return pieces


def _join(pieces: list[str]) -> str:
    return "".join(p if p.endswith("\n") else p + " " for p in pieces).strip()


def chunk_text(text: str, size: int, overlap: int) -> list[str]:
    text = _clean(text)
    if len(text) <= size:
        return [text] if text else []
    pieces = _pieces(text)
    chunks: list[str] = []
    current: list[str] = []
    length = 0
    for piece in pieces:
        # очень длинное «предложение» (таблица, список без точек) режем жёстко
        while len(piece) > size:
            head, piece = piece[:size], piece[size - overlap:]
            if current:
                chunks.append(_join(current))
                current, length = [], 0
            chunks.append(head)
        if length + len(piece) > size and current:
            chunks.append(_join(current))
            # перекрытие: переносим хвост предыдущего фрагмента
            tail, tail_len = [], 0
            for prev in reversed(current):
                if tail_len + len(prev) > overlap:
                    break
                tail.insert(0, prev)
                tail_len += len(prev) + 1
            current, length = tail, tail_len
        current.append(piece)
        length += len(piece) + 1
    if current:
        chunks.append(_join(current))
    return [c for c in chunks if c.strip()]


def chunk_pages(doc_id: str, pages: list[dict], size: int, overlap: int) -> list[dict]:
    chunks = []
    for page in pages:
        for piece in chunk_text(page["text"], size, overlap):
            chunks.append({
                "id": f"{doc_id}:{len(chunks)}",
                "doc_id": doc_id,
                "idx": len(chunks),
                "loc": page["loc"],
                "text": piece,
            })
    return chunks
