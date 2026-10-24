"""Веб-сервер Mind AI AI: REST API + веб-интерфейс + (опционально) Telegram-бот."""
import asyncio
import json
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import insights, llm, rag
from . import firebase_auth, mailer
from .chats import chats
from .auth import COOKIE, SESSION_DAYS, AuthError, limiter, public_user, users
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


def current_user(request: Request) -> dict | None:
    return users.user_by_token(request.cookies.get(COOKIE))


def owner_of(request: Request) -> str:
    """Каждый пользователь видит только свои документы."""
    user = current_user(request)
    if not user:
        raise HTTPException(401, "Требуется вход")
    return f"user:{user['id']}"


def public(doc: dict) -> dict:
    return {k: v for k, v in doc.items() if k not in ("owner", "summary", "cache")}


@app.get("/")
async def index(request: Request):
    if not current_user(request):
        return RedirectResponse("/login")
    return FileResponse(settings.web_dir / "index.html")


@app.get("/login")
async def login_page(request: Request):
    if current_user(request):
        return RedirectResponse("/")
    return FileResponse(settings.web_dir / "login.html")


# ---------------------------------------------------------------- аккаунты

def client_ip(request: Request) -> str:
    """IP клиента. Заголовки прокси учитываем, только если запрос пришёл с локального туннеля."""
    host = request.client.host if request.client else "?"
    if host in ("127.0.0.1", "::1"):
        forwarded = request.headers.get("cf-connecting-ip") or request.headers.get("x-forwarded-for", "")
        if forwarded:
            return forwarded.split(",")[0].strip()
    return host


def auth_error(exc: AuthError, status: int = 400) -> HTTPException:
    return HTTPException(status, str(exc))


class RegisterBody(BaseModel):
    name: str = Field(max_length=80)
    email: str = Field(max_length=120)
    password: str = Field(max_length=128)
    lang: str = "ru"


class LoginBody(BaseModel):
    email: str = Field(max_length=120)
    password: str = Field(max_length=128)


class CodeBody(BaseModel):
    email: str = Field(max_length=120)
    code: str = Field(max_length=12)


class EmailBody(BaseModel):
    email: str = Field(max_length=120)
    kind: str = "verify"
    lang: str = "ru"


class ResetBody(BaseModel):
    email: str = Field(max_length=120)
    code: str = Field(max_length=12)
    password: str = Field(max_length=128)


def _signed_in(user: dict, request: Request) -> JSONResponse:
    resp = JSONResponse(public_user(user))
    resp.set_cookie(COOKIE, users.create_session(user), max_age=SESSION_DAYS * 86400, httponly=True,
                    samesite="lax", secure=request.url.scheme == "https")
    return resp


async def _send(user: dict, kind: str, code: str, lang: str) -> None:
    try:
        await asyncio.to_thread(mailer.send_code, user["email"], kind, code, user["name"], lang)
    except Exception:  # noqa: BLE001
        log.exception("Не удалось отправить письмо")
        raise HTTPException(502, "mail_failed")


@app.post("/api/auth/register")
async def register(body: RegisterBody, request: Request):
    try:
        limiter.hit("register", client_ip(request))
        user, code = await asyncio.to_thread(users.register, body.name, body.email, body.password)
    except AuthError as exc:
        raise auth_error(exc, 429 if str(exc) == "too_many" else 400)
    await _send(user, "verify", code, body.lang)
    return {"need_verify": True, "email": user["email"], "mail": mailer.mode()}


@app.post("/api/auth/verify")
async def verify(body: CodeBody, request: Request):
    try:
        limiter.hit("code", client_ip(request))
        user = users.verify_email(body.email, body.code)
    except AuthError as exc:
        raise auth_error(exc)
    return _signed_in(user, request)


@app.post("/api/auth/send-code")
async def send_code(body: EmailBody, request: Request):
    """Повторный код подтверждения или код сброса пароля. Всегда отвечает ok — не раскрываем, есть ли email."""
    try:
        limiter.hit("code", client_ip(request))
        found = users.resend(body.email, "reset" if body.kind == "reset" else "verify")
    except AuthError as exc:
        raise auth_error(exc, 429)
    if found:
        await _send(found[0], body.kind, found[1], body.lang)
    return {"ok": True, "mail": mailer.mode()}


@app.post("/api/auth/reset")
async def reset(body: ResetBody, request: Request):
    try:
        limiter.hit("code", client_ip(request))
        user = await asyncio.to_thread(users.reset_password, body.email, body.code, body.password)
    except AuthError as exc:
        raise auth_error(exc)
    return _signed_in(user, request)


@app.post("/api/auth/login")
async def login(body: LoginBody, request: Request):
    try:
        limiter.hit("login", client_ip(request))
        user = await asyncio.to_thread(users.login, body.email, body.password)
    except AuthError as exc:
        if str(exc) == "invalid":
            await asyncio.sleep(0.5)  # замедляем перебор паролей
        raise auth_error(exc, {"invalid": 401, "not_verified": 403, "locked": 423, "too_many": 429}.get(str(exc), 400))
    return _signed_in(user, request)


class FirebaseBody(BaseModel):
    id_token: str = Field(max_length=4096)
    name: str = Field(default="", max_length=80)


@app.get("/api/auth/config")
async def auth_config():
    return {"firebase": firebase_auth.public_config()}


@app.post("/api/auth/check-email")
async def check_email(body: EmailBody, request: Request):
    """Проверка до регистрации в Firebase: формат, одноразовые ящики, Gmail-алиасы."""
    try:
        limiter.hit("register", client_ip(request))
        users.email_available(body.email)
    except AuthError as exc:
        raise auth_error(exc, 429 if str(exc) == "too_many" else 400)
    return {"ok": True}


@app.post("/api/auth/firebase")
async def firebase_login(body: FirebaseBody, request: Request):
    if not firebase_auth.enabled():
        raise HTTPException(404, "firebase_disabled")
    try:
        limiter.hit("login", client_ip(request))
        claims = await asyncio.to_thread(firebase_auth.verify, body.id_token)
        user = users.firebase_login(claims["user_id"], claims["email"], body.name or claims.get("name", ""))
    except AuthError as exc:
        raise auth_error(exc, 429 if str(exc) == "too_many" else 400)
    except ValueError as exc:
        raise HTTPException(401, "not_verified" if "not_verified" in str(exc) else "invalid")
    return _signed_in(user, request)


@app.post("/api/auth/logout")
async def logout(request: Request):
    users.drop_session(request.cookies.get(COOKIE))
    resp = JSONResponse({"ok": True})
    resp.delete_cookie(COOKIE)
    return resp


@app.get("/api/auth/me")
async def me(request: Request):
    user = current_user(request)
    if not user:
        raise HTTPException(401, "Требуется вход")
    return public_user(user)


# ---------------------------------------------------------------- профиль и настройки

class ProfileBody(BaseModel):
    name: str = Field(max_length=80)


class PasswordBody(BaseModel):
    old: str = Field(max_length=128)
    new: str = Field(max_length=128)


class DeleteAccountBody(BaseModel):
    password: str = Field(default="", max_length=128)


def _require_user(request: Request) -> dict:
    user = current_user(request)
    if not user:
        raise HTTPException(401, "Требуется вход")
    return user


@app.put("/api/settings")
async def save_settings(values: dict, request: Request):
    return users.update_settings(_require_user(request), values)


@app.put("/api/profile")
async def save_profile(body: ProfileBody, request: Request):
    user = _require_user(request)
    try:
        users.update_profile(user, body.name)
    except AuthError as exc:
        raise auth_error(exc)
    return public_user(user)


@app.post("/api/profile/password")
async def change_password(body: PasswordBody, request: Request):
    user = _require_user(request)
    if user.get("guest"):
        raise HTTPException(400, "guest")
    try:
        await asyncio.to_thread(users.change_password, user, body.old, body.new)
    except AuthError as exc:
        raise auth_error(exc)
    return _signed_in(user, request)  # старые сессии закрыты, текущей выдаём новую


@app.post("/api/profile/delete")
async def delete_account(body: DeleteAccountBody, request: Request):
    user = _require_user(request)
    if not user.get("guest") and user.get("hash"):  # у аккаунтов Firebase/Google локального пароля нет
        try:
            await asyncio.to_thread(users.login, user["email"], body.password)
        except AuthError:
            raise HTTPException(401, "invalid")
    owner = f"user:{user['id']}"
    store.delete_owner(owner)
    chats.delete_owner(owner)
    users.delete(user)
    resp = JSONResponse({"ok": True})
    resp.delete_cookie(COOKIE)
    return resp


@app.delete("/api/documents")
async def delete_all_documents(request: Request):
    return {"deleted": store.delete_owner(owner_of(request))}


@app.get("/api/status")
async def status():
    return {
        "app": settings.app_name,
        "llm_enabled": settings.llm_enabled,
        "llm_provider": settings.llm_provider,
        "llm_model": settings.llm_model if settings.llm_enabled else None,
        "ocr": ocr_engine(),
        "telegram": bool(settings.telegram_token),
        "mail": mailer.mode(),
        "version": "1.0",
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
async def document_file(doc_id: str, request: Request):
    doc = store.get(doc_id, owner_of(request))
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
async def evidence(chunk: str, request: Request, q: str = ""):
    """Страница PDF с подсветкой строк-доказательств."""
    found = store.get_chunk(chunk)
    doc = store.get(found["doc_id"], owner_of(request)) if found else None
    if not doc:
        raise HTTPException(404, "Фрагмент не найден")
    png = await asyncio.to_thread(insights.render_evidence, doc, found, q[:2000])
    if not png:
        raise HTTPException(404, "Для этого формата нет изображения страницы")
    return Response(png, media_type="image/png", headers={"Cache-Control": "private, max-age=3600"})


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    doc_ids: list[str] | None = None
    chat_id: str | None = None


@app.post("/api/ask")
async def ask(body: AskRequest, request: Request):
    owner = owner_of(request)
    prefs = (current_user(request) or {}).get("settings", {})

    def sse(event: dict) -> str:
        return f"data: {json.dumps(event, ensure_ascii=False)}\n\n"

    async def events():
        chat = chats.get(body.chat_id, owner) if body.chat_id else None
        if not chat:
            chat = chats.create(owner)
            yield sse({"type": "chat", "id": chat["id"]})
        key = f"{owner}:{chat['id']}"
        if not rag.history.get(key):  # после перезапуска сервера восстанавливаем контекст диалога из сохранённого чата
            msgs = chat["messages"]
            for q, a in zip(msgs[::2], msgs[1::2]):
                rag.history.add(key, q["text"], a["text"])
        parts, sources, cited = [], [], []
        try:
            async for event in rag.answer_stream(body.question, owner, key, body.doc_ids, prefs):
                if event["type"] == "delta":
                    parts.append(event["text"])
                elif event["type"] == "sources":
                    sources = event["sources"]
                elif event["type"] == "done":
                    cited = event.get("cited", [])
                yield sse(event)
        except Exception as exc:  # noqa: BLE001
            log.exception("Ошибка ответа")
            yield sse({"type": "error", "message": str(exc)})
        if parts:
            by_n = {x["n"]: x for x in sources}
            chats.add_exchange(chat["id"], body.question, "".join(parts).strip(), [by_n[n] for n in cited if n in by_n])

    return StreamingResponse(events(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


# ---------------------------------------------------------------- сохранённые чаты

class ChatTitle(BaseModel):
    title: str = Field(min_length=1, max_length=80)


@app.get("/api/chats")
async def list_chats(request: Request):
    return chats.list(owner_of(request))


@app.get("/api/chats/{chat_id}")
async def get_chat(chat_id: str, request: Request):
    chat = chats.get(chat_id, owner_of(request))
    if not chat:
        raise HTTPException(404, "Чат не найден")
    return {"id": chat["id"], "title": chat["title"], "messages": chat["messages"]}


@app.patch("/api/chats/{chat_id}")
async def rename_chat(chat_id: str, body: ChatTitle, request: Request):
    if not chats.rename(chat_id, owner_of(request), body.title):
        raise HTTPException(404, "Чат не найден")
    return {"ok": True}


@app.delete("/api/chats/{chat_id}")
async def delete_chat(chat_id: str, request: Request):
    owner = owner_of(request)
    if not chats.delete(chat_id, owner):
        raise HTTPException(404, "Чат не найден")
    rag.history.clear(f"{owner}:{chat_id}")
    return {"ok": True}


@app.delete("/api/chats")
async def delete_all_chats(request: Request):
    owner = owner_of(request)
    for chat in chats.list(owner):
        rag.history.clear(f"{owner}:{chat['id']}")
    return {"deleted": chats.delete_owner(owner)}


def main():
    import uvicorn
    uvicorn.run("app.main:app", host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
