"""Сохранённые чаты: у каждого пользователя свой список диалогов с сообщениями и источниками."""
from __future__ import annotations

import json
import secrets
import threading
import time
from pathlib import Path

from .config import settings

MAX_MESSAGES = 400  # на один чат — чтобы файл не рос бесконечно


class ChatStore:
    def __init__(self, path: Path):
        self.path = path
        self.lock = threading.RLock()
        self.chats: dict[str, dict] = {}
        if path.exists():
            self.chats = json.loads(path.read_text("utf-8")).get("chats", {})

    def _save(self) -> None:
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"chats": self.chats}, ensure_ascii=False), "utf-8")
        tmp.replace(self.path)

    def list(self, owner: str) -> list[dict]:
        with self.lock:
            items = [c for c in self.chats.values() if c["owner"] == owner]
        items.sort(key=lambda c: c["updated"], reverse=True)
        return [{"id": c["id"], "title": c["title"], "updated": c["updated"], "count": len(c["messages"])} for c in items]

    def get(self, chat_id: str, owner: str) -> dict | None:
        chat = self.chats.get(chat_id)
        return chat if chat and chat["owner"] == owner else None

    def create(self, owner: str, title: str = "") -> dict:
        now = time.time()
        chat = {"id": secrets.token_hex(8), "owner": owner, "title": title.strip()[:80],
                "created": now, "updated": now, "messages": []}
        with self.lock:
            self.chats[chat["id"]] = chat
            self._save()
        return chat

    def add_exchange(self, chat_id: str, question: str, answer: str, sources: list[dict]) -> None:
        """Сохраняет вопрос и ответ. Из источников храним только то, что нужно для ссылок."""
        keep = ("n", "chunk_id", "doc_id", "doc_name", "loc", "loc_label")
        with self.lock:
            chat = self.chats.get(chat_id)
            if not chat:
                return
            now = time.time()
            chat["messages"] += [
                {"role": "user", "text": question, "ts": now},
                {"role": "bot", "text": answer, "ts": now, "sources": [{k: s.get(k) for k in keep} for s in sources]},
            ]
            del chat["messages"][:-MAX_MESSAGES]
            if not chat["title"]:
                chat["title"] = question.strip().replace("\n", " ")[:80]
            chat["updated"] = now
            self._save()

    def rename(self, chat_id: str, owner: str, title: str) -> bool:
        with self.lock:
            chat = self.get(chat_id, owner)
            if not chat or not title.strip():
                return False
            chat["title"] = title.strip()[:80]
            self._save()
            return True

    def delete(self, chat_id: str, owner: str) -> bool:
        with self.lock:
            if not self.get(chat_id, owner):
                return False
            del self.chats[chat_id]
            self._save()
            return True

    def delete_owner(self, owner: str) -> int:
        with self.lock:
            ids = [cid for cid, c in self.chats.items() if c["owner"] == owner]
            for cid in ids:
                del self.chats[cid]
            if ids:
                self._save()
            return len(ids)


chats = ChatStore(settings.data_dir / "chats.json")
