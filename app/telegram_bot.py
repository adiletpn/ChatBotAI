"""Telegram-бот DocMind AI (aiogram 3). Запускается вместе с сервером, если задан TELEGRAM_BOT_TOKEN.

Каждый чат имеет свой набор документов. Команды:
  /start — приветствие и инструкция    /docs — список документов
  /summary — краткое содержание         /clear — удалить документы и историю
"""
import asyncio
import html
import io
import logging
import re

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ChatAction, ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from . import rag
from .config import settings
from .parsers import UnsupportedFormat
from .store import store

log = logging.getLogger(__name__)
dp = Dispatcher()

TEXTS = {
    "start": {
        "kk": "Сәлем! Мен <b>DocMind AI</b> — құжаттар бойынша сұрақтарға жауап беретін чат-ботпын.\n\n"
              "1️⃣ Маған PDF, DOCX, PPTX, XLSX, TXT файлын немесе құжаттың фотосын жіберіңіз.\n"
              "2️⃣ Құжат бойынша сұрақ қойыңыз — қазақша, орысша немесе ағылшынша.\n"
              "3️⃣ Мен жауап беремін және дереккөзін (бетін) көрсетемін.\n\n"
              "/docs — құжаттар тізімі, /summary — қысқаша мазмұны, /clear — тазалау",
        "ru": "Привет! Я <b>DocMind AI</b> — чат-бот, который отвечает на вопросы по вашим документам.\n\n"
              "1️⃣ Отправьте мне файл PDF, DOCX, PPTX, XLSX, TXT или фото документа.\n"
              "2️⃣ Задайте вопрос по документу — на казахском, русском или английском.\n"
              "3️⃣ Я отвечу и укажу источник (страницу).\n\n"
              "/docs — список документов, /summary — краткое содержание, /clear — очистить",
    },
    "processing": {"kk": "⏳ Құжат өңделуде: {name}", "ru": "⏳ Обрабатываю документ: {name}"},
    "ready": {
        "kk": "✅ <b>{name}</b> жүктелді: {pages} бет/бөлім, {chunks} фрагмент{ocr}.\nЕнді сұрақ қоя аласыз!",
        "ru": "✅ <b>{name}</b> загружен: {pages} стр./разделов, {chunks} фрагментов{ocr}.\nТеперь можно задавать вопросы!",
    },
    "ocr": {"kk": ", OCR арқылы танылған беттер: {n}", "ru": ", распознано OCR страниц: {n}"},
    "error": {"kk": "❌ Файлды оқу мүмкін болмады: {err}", "ru": "❌ Не удалось прочитать файл: {err}"},
    "too_big": {"kk": "❌ Файл тым үлкен (Telegram шектеуі 20 МБ).", "ru": "❌ Файл слишком большой (лимит Telegram — 20 МБ)."},
    "no_docs": {"kk": "Құжаттар жоқ. Файл жіберіңіз.", "ru": "Документов нет. Отправьте файл."},
    "cleared": {"kk": "🗑 Барлық құжаттар мен тарих өшірілді.", "ru": "🗑 Все документы и история удалены."},
    "sources": {"kk": "Дереккөздер", "ru": "Источники"},
}


def tr(key: str, lang: str, **kwargs) -> str:
    variants = TEXTS[key]
    text = variants.get(lang) or variants["ru"]
    return text.format(**kwargs) if kwargs else text


def ui_lang(message: Message) -> str:
    code = (message.from_user.language_code or "") if message.from_user else ""
    return "kk" if code.startswith("kk") else "ru"


def owner(message: Message) -> str:
    return f"tg:{message.chat.id}"


def md_to_html(text: str) -> str:
    """Минимальная конвертация markdown-ответа модели в HTML Telegram."""
    text = html.escape(text)
    text = re.sub(r"```(?:\w+)?\n?(.*?)```", r"<pre>\1</pre>", text, flags=re.S)
    text = re.sub(r"`([^`\n]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", text)
    text = re.sub(r"(?<!\w)_(?!\s)(.+?)(?<!\s)_(?!\w)", r"<i>\1</i>", text)
    text = re.sub(r"^#{1,6}\s*(.+)$", r"<b>\1</b>", text, flags=re.M)
    text = re.sub(r"^\s*[-*]\s+", "• ", text, flags=re.M)
    text = re.sub(r"^\|?[\s:|-]+\|[\s:|-]*$", "", text, flags=re.M)  # разделители таблиц
    return text


async def send_long(message: Message, text: str) -> None:
    while text:
        part = text[:4000]
        if len(text) > 4000 and "\n" in part:
            part = part[: part.rfind("\n")]
        try:
            await message.answer(part)
        except Exception:  # noqa: BLE001 — если HTML сломался, отправляем как есть
            await message.answer(re.sub(r"<[^>]+>", "", part), parse_mode=None)
        text = text[len(part):].lstrip()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(tr("start", ui_lang(message)))


@dp.message(Command("docs"))
async def cmd_docs(message: Message):
    docs = store.list(owner(message))
    if not docs:
        await message.answer(tr("no_docs", ui_lang(message)))
        return
    lines = [f"📄 <b>{html.escape(d['name'])}</b> — {d['pages']} / {d['chunks']}" for d in docs]
    await message.answer("\n".join(lines))


@dp.message(Command("clear"))
async def cmd_clear(message: Message):
    store.delete_owner(owner(message))
    rag.history.clear(owner(message))
    await message.answer(tr("cleared", ui_lang(message)))


@dp.message(Command("summary"))
async def cmd_summary(message: Message):
    lang = ui_lang(message)
    docs = store.list(owner(message))
    if not docs:
        await message.answer(tr("no_docs", lang))
        return
    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    doc = docs[-1]
    result = await rag.summarize(doc, lang)
    questions = "\n".join(f"❓ {html.escape(q)}" for q in result.get("questions", []))
    await send_long(message, f"📄 <b>{html.escape(doc['name'])}</b>\n\n{html.escape(result['summary'])}\n\n{questions}")


async def _ingest(message: Message, filename: str, file_id: str, size: int | None):
    lang = ui_lang(message)
    if size and size > 20 * 1024 * 1024:
        await message.answer(tr("too_big", lang))
        return
    status = await message.answer(tr("processing", lang, name=html.escape(filename)))
    buf = io.BytesIO()
    await message.bot.download(file_id, destination=buf)
    try:
        doc = await asyncio.to_thread(rag.ingest, owner(message), filename, buf.getvalue())
    except (UnsupportedFormat, ValueError) as exc:
        await status.edit_text(tr("error", lang, err=html.escape(str(exc))))
        return
    except Exception as exc:  # noqa: BLE001
        log.exception("Ошибка обработки файла в Telegram")
        await status.edit_text(tr("error", lang, err=html.escape(str(exc)[:200])))
        return
    ocr = tr("ocr", lang, n=doc["ocr_pages"]) if doc["ocr_pages"] else ""
    await status.edit_text(tr("ready", lang, name=html.escape(doc["name"]), pages=doc["pages"],
                              chunks=doc["chunks"], ocr=ocr))


@dp.message(F.document)
async def on_document(message: Message):
    doc = message.document
    await _ingest(message, doc.file_name or "document", doc.file_id, doc.file_size)


@dp.message(F.photo)
async def on_photo(message: Message):
    photo = message.photo[-1]  # самое большое разрешение
    await _ingest(message, f"photo_{message.message_id}.jpg", photo.file_id, photo.file_size)


@dp.message(F.text)
async def on_question(message: Message):
    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    result = await rag.answer(message.text, owner(message), owner(message))
    text = md_to_html(result["text"])
    if result["sources"]:
        lang = result["lang"] if result["lang"] in ("kk", "ru") else "ru"
        lines = []
        for s in result["sources"][:5]:
            loc = f", {s['loc_label']}" if s["loc_label"] else ""
            lines.append(f"[{s['n']}] {html.escape(s['doc_name'])}{html.escape(loc)}")
        text += f"\n\n📚 <b>{tr('sources', lang)}:</b>\n" + "\n".join(lines)
    await send_long(message, text)


async def run_bot():
    bot = Bot(settings.telegram_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    try:
        await dp.start_polling(bot, handle_signals=False)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_bot())
