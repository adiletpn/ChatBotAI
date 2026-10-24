"""Веб-сервер DocMind AI: REST API + веб-интерфейс + (опционально) Telegram-бот."""
import asyncio
import json
import logging
import re
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import insights, llm, rag
from .config import settings
from .lang import format_loc
from .ocr import ocr_engine
from .parsers import SUPPORTED_EXT, UnsupportedFormat
from .store import store

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("docmind")


@asynccontextmanager
async def lifespan(app: FastAPI):
    bot_task = None
    if settings.telegram_token:
        from .telegram_bot import run_bot
        bot_task = asyncio.create_task(run_bot())
        log.info("Telegram-бот запущен")
    log.info("LLM: %s (%s, %s)", "включена" if settings.llm_enabled else "ОФЛАЙН-РЕЖИМ",
             settings.llm_model, settings.llm_base_url)
    log.info("OCR: %s", ocr_engine())
    yield
    if bot_task:
        bot_task.cancel()


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.mount("/static", StaticFiles(directory=settings.web_dir), name="static")


def owner_of(request: Request) -> str:
    """Каждый браузер работает со своим набором документов (id сессии хранится в localStorage)."""
    sid = request.headers.get("X-Session-Id", "")
    if not re.fullmatch(r"[A-Za-z0-9_-]{8,64}", sid):
        raise HTTPException(400, "Нет X-Session-Id")
    return f"web:{sid}"


def public(doc: dict) -> dict:
    return {k: v for k, v in doc.items() if k not in ("owner", "summary", "cache")}


@app.get("/")
async def index():
    return FileResponse(settings.web_dir / "index.html")


@app.get("/api/status")
async def status():
    return {
        "app": settings.app_name,
        "llm_enabled": settings.llm_enabled,
        "llm_provider": settings.llm_provider,
        "llm_model": settings.llm_model if settings.llm_enabled else None,
        "ocr": ocr_engine(),
        "telegram": bool(settings.telegram_token),
        "formats": sorted(SUPPORTED_EXT),
        "max_upload_mb": settings.max_upload_mb,
    }


@app.get("/api/llm-check")
async def llm_check():
    return await llm.check()


@app.get("/api/documents")
async def list_documents(request: Request):
    return [public(d) for d in store.list(owner_of(request))]


@app.post("/api/documents")
async def upload(request: Request, files: list[UploadFile] = File(...)):
    owner = owner_of(request)
    results = []
    for file in files:
        data = await file.read()
        name = file.filename or "document"
        if len(data) > settings.max_upload_mb * 1024 * 1024:
            results.append({"name": name, "error": f"Файл больше {settings.max_upload_mb} МБ"})
            continue
        try:
            doc = await asyncio.to_thread(rag.ingest, owner, name, data)
            results.append(public(doc))
        except UnsupportedFormat as exc:
            results.append({"name": name, "error": str(exc)})
        except Exception as exc:  # noqa: BLE001
            log.exception("Ошибка обработки %s", name)
            results.append({"name": name, "error": f"Не удалось прочитать файл: {exc}"})
    return results


@app.delete("/api/documents/{doc_id}")
async def delete_document(doc_id: str, request: Request):
    if not store.get(doc_id, owner_of(request)):
        raise HTTPException(404, "Документ не найден")
    store.delete(doc_id)
    return {"ok": True}


@app.get("/api/documents/{doc_id}/file")
async def document_file(doc_id: str, session: str):
    doc = store.get(doc_id, f"web:{session}")
    if not doc:
        raise HTTPException(404, "Документ не найден")
    return FileResponse(store.file_path(doc), filename=doc["name"],
                        content_disposition_type="inline")


@app.get("/api/documents/{doc_id}/summary")
async def document_summary(doc_id: str, request: Request, lang: str = "ru"):
    doc = store.get(doc_id, owner_of(request))
    if not doc:
        raise HTTPException(404, "Документ не найден")
    return await rag.summarize(doc, lang if lang in ("kk", "ru", "en") else "ru")


def _lang(lang: str) -> str:
    return lang if lang in ("kk", "ru", "en") else "ru"


@app.get("/api/documents/{doc_id}/insights")
async def document_insights(doc_id: str, request: Request, lang: str = "ru"):
    doc = store.get(doc_id, owner_of(request))
    if not doc:
        raise HTTPException(404, "Документ не найден")
    return await insights.insights(doc, _lang(lang))


@app.get("/api/documents/{doc_id}/quiz")
async def document_quiz(doc_id: str, request: Request, lang: str = "ru", n: int = 5):
    doc = store.get(doc_id, owner_of(request))
    if not doc:
        raise HTTPException(404, "Документ не найден")
    return await insights.quiz(doc, _lang(lang), max(3, min(n, 10)))


@app.get("/api/chunk")
async def chunk_info(chunk: str, request: Request, lang: str = "ru"):
    found = store.get_chunk(chunk)
    doc = store.get(found["doc_id"], owner_of(request)) if found else None
    if not doc:
        raise HTTPException(404, "Фрагмент не найден")
    return {
        "chunk_id": found["id"], "doc_id": doc["id"], "doc_name": doc["name"], "text": found["text"],
        "loc": found["loc"], "loc_label": format_loc(found["loc"], _lang(lang)),
        "has_page": doc["ext"] == ".pdf" and found["loc"].get("type") == "page",
    }


@app.get("/api/evidence.png")
async def evidence(session: str, chunk: str, q: str = ""):
    """Страница PDF с подсветкой строк-доказательств (картинка, поэтому session — в query)."""
    found = store.get_chunk(chunk)
    doc = store.get(found["doc_id"], f"web:{session}") if found else None
    if not doc:
        raise HTTPException(404, "Фрагмент не найден")
    png = await asyncio.to_thread(insights.render_evidence, doc, found, q[:2000])
    if not png:
        raise HTTPException(404, "Для этого формата нет изображения страницы")
    return Response(png, media_type="image/png", headers={"Cache-Control": "private, max-age=3600"})


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    doc_ids: list[str] | None = None


@app.post("/api/ask")
async def ask(body: AskRequest, request: Request):
    owner = owner_of(request)

    async def events():
        try:
            async for event in rag.answer_stream(body.question, owner, owner, body.doc_ids):
                yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
        except Exception as exc:  # noqa: BLE001
            log.exception("Ошибка ответа")
            yield f"data: {json.dumps({'type': 'error', 'message': str(exc)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(events(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.post("/api/clear")
async def clear_history(request: Request):
    rag.history.clear(owner_of(request))
    return {"ok": True}


def main():
    import uvicorn
    uvicorn.run("app.main:app", host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
