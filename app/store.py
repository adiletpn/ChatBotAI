"""Хранилище документов и фрагментов: JSON-файл на диске + поисковый индекс в памяти."""
from __future__ import annotations

import json
import threading
import time
import uuid
from pathlib import Path

from .config import settings
from .lang import detect_lang
from .retriever import BM25Index
from .semantic import semantic


class DocumentStore:
    def __init__(self, path: Path):
        self.path = path
        self.lock = threading.RLock()
        self.documents: dict[str, dict] = {}
        self.chunks: list[dict] = []
        self.index = BM25Index()
        self._load()

    def _load(self) -> None:
        if self.path.exists():
            data = json.loads(self.path.read_text("utf-8"))
            self.documents = {d["id"]: d for d in data.get("documents", [])}
            self.chunks = data.get("chunks", [])
        self.index.build(self.chunks)

    def _save(self) -> None:
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"documents": list(self.documents.values()), "chunks": self.chunks},
                                  ensure_ascii=False), "utf-8")
        tmp.replace(self.path)

    @staticmethod
    def new_id() -> str:
        return uuid.uuid4().hex[:12]

    def add(self, doc_id: str, owner: str, name: str, ext: str, size: int, pages: list[dict], chunks: list[dict]) -> dict:
        full_text = "\n".join(p["text"] for p in pages)
        doc = {
            "id": doc_id,
            "owner": owner,
            "name": name,
            "ext": ext,
            "size": size,
            "created": time.time(),
            "pages": len(pages),
            "ocr_pages": sum(1 for p in pages if p.get("ocr")),
            "chars": len(full_text),
            "chunks": len(chunks),
            "lang": detect_lang(full_text[:5000]),
            "summary": {},
        }
        with self.lock:
            self.documents[doc_id] = doc
            self.chunks.extend(chunks)
            self.index.build(self.chunks)
            self._save()
        semantic.add(chunks)
        return doc

    def list(self, owner: str) -> list[dict]:
        with self.lock:
            docs = [d for d in self.documents.values() if d["owner"] == owner]
        return sorted(docs, key=lambda d: d["created"])

    def get(self, doc_id: str, owner: str | None = None) -> dict | None:
        doc = self.documents.get(doc_id)
        if doc and owner is not None and doc["owner"] != owner:
            return None
        return doc

    def doc_chunks(self, doc_ids: set[str]) -> list[dict]:
        with self.lock:
            return [c for c in self.chunks if c["doc_id"] in doc_ids]

    def set_summary(self, doc_id: str, lang: str, summary: dict) -> None:
        with self.lock:
            if doc_id in self.documents:
                self.documents[doc_id]["summary"][lang] = summary
                self._save()

    def set_cache(self, doc_id: str, key: str, value) -> None:
        """Кэш результатов LLM по документу (карта документа, тест) — чтобы не платить за повторные запросы."""
        with self.lock:
            if doc_id in self.documents:
                self.documents[doc_id].setdefault("cache", {})[key] = value
                self._save()

    def get_chunk(self, chunk_id: str) -> dict | None:
        with self.lock:
            return next((c for c in self.chunks if c["id"] == chunk_id), None)

    def file_path(self, doc: dict) -> Path:
        return settings.upload_dir / f"{doc['id']}{doc['ext']}"

    def delete(self, doc_id: str) -> None:
        with self.lock:
            doc = self.documents.pop(doc_id, None)
            if not doc:
                return
            semantic.remove(c["id"] for c in self.chunks if c["doc_id"] == doc_id)
            self.chunks = [c for c in self.chunks if c["doc_id"] != doc_id]
            self.index.build(self.chunks)
            self._save()
        self.file_path(doc).unlink(missing_ok=True)

    def delete_owner(self, owner: str) -> int:
        ids = [d["id"] for d in self.list(owner)]
        for doc_id in ids:
            self.delete(doc_id)
        return len(ids)


store = DocumentStore(settings.store_file)
