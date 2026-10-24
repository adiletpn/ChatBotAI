"""Семантический поиск: векторы смысла (эмбеддинги) для фрагментов документов.

BM25 находит совпадения слов, а эмбеддинги — совпадение смысла: «когда дают деньги за работу»
находит «заработная плата выплачивается 10 и 25 числа», и даже между языками.
Модель paraphrase-multilingual-MiniLM-L12-v2 (ONNX, ~220 МБ) работает локально, без внешних API.
Загружается в фоне при старте; пока она не готова (или не установлена) — поиск идёт только по BM25.
"""
from __future__ import annotations

import logging
import threading

from .config import settings

log = logging.getLogger(__name__)

MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
MIN_SCORE = 0.35  # ниже — смысловой связи практически нет
PIECE_CHARS = 300  # модель видит ~128 токенов, поэтому фрагмент режется на куски по 1-3 предложения


def _pieces(text: str) -> list[str]:
    from .chunker import split_sentences

    pieces, current = [], ""
    for sentence in split_sentences(text):
        if current and len(current) + len(sentence) > PIECE_CHARS:
            pieces.append(current)
            current = ""
        current = f"{current} {sentence}".strip()
    if current:
        pieces.append(current)
    return pieces or [text[:PIECE_CHARS]]


class SemanticIndex:
    def __init__(self):
        self.lock = threading.RLock()
        self.model = None
        self.ready = False
        self.error = ""
        self.vectors: dict[str, "np.ndarray"] = {}  # chunk_id -> матрица нормированных векторов его кусков

    # ------------------------------------------------------------ модель

    def start(self, chunks_provider) -> None:
        """Загружает модель в фоновом потоке и считает векторы для уже загруженных документов."""
        if not settings.semantic_search:
            self.error = "выключен (SEMANTIC_SEARCH=false)"
            return
        threading.Thread(target=self._load, args=(chunks_provider,), daemon=True).start()

    def _load(self, chunks_provider) -> None:
        try:
            from fastembed import TextEmbedding

            self.model = TextEmbedding(MODEL, cache_dir=str(settings.models_dir))
            self._add(chunks_provider())
            self.ready = True  # только после векторов уже загруженных документов
            self._add(chunks_provider())  # документы, загруженные, пока считались векторы
            log.info("Семантический поиск готов: %d фрагментов", len(self.vectors))
        except Exception as exc:  # noqa: BLE001 — без модели бот продолжает работать на BM25
            self.error = f"{type(exc).__name__}: {exc}"[:200]
            log.warning("Семантический поиск недоступен: %s", self.error)

    def _embed(self, texts: list[str]):
        import numpy as np

        matrix = np.array(list(self.model.embed(texts, batch_size=32)), dtype=np.float32)
        matrix /= np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-9
        return matrix

    # ------------------------------------------------------------ индекс

    def add(self, chunks: list[dict]) -> None:
        if self.ready:
            self._add(chunks)

    def _add(self, chunks: list[dict]) -> None:
        todo = [c for c in chunks if c["id"] not in self.vectors]
        if not todo:
            return
        pieces = [_pieces(c["text"]) for c in todo]
        matrix = self._embed([p for group in pieces for p in group])
        start = 0
        with self.lock:
            for chunk, group in zip(todo, pieces):
                self.vectors[chunk["id"]] = matrix[start:start + len(group)]
                start += len(group)

    def remove(self, chunk_ids) -> None:
        with self.lock:
            for chunk_id in chunk_ids:
                self.vectors.pop(chunk_id, None)

    def search(self, queries: list[str], chunks: list[dict], top_k: int) -> list[tuple[dict, float]]:
        """Косинусная близость запроса (и его переводов) к фрагментам; берётся лучший из запросов."""
        queries = [q for q in queries if q.strip()]
        if not (self.ready and queries and chunks):
            return []
        import numpy as np

        with self.lock:
            pairs = [(c, self.vectors[c["id"]]) for c in chunks if c["id"] in self.vectors]
        if not pairs:
            return []
        q = self._embed(queries)
        owner = np.concatenate([np.full(len(v), i) for i, (_, v) in enumerate(pairs)])
        piece_scores = (np.concatenate([v for _, v in pairs]) @ q.T).max(axis=1)
        scores = np.full(len(pairs), -1.0, dtype=np.float32)
        np.maximum.at(scores, owner, piece_scores)  # балл фрагмента — лучший из его кусков
        order = np.argsort(-scores)[:top_k]
        return [(pairs[i][0], float(scores[i])) for i in order if scores[i] >= MIN_SCORE]

    def status(self) -> dict:
        return {"ready": self.ready, "model": MODEL.split("/")[-1], "chunks": len(self.vectors), "error": self.error}


semantic = SemanticIndex()
