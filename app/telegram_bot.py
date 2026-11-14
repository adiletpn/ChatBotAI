"""Telegram-бот Mind AI (aiogram 3). Запускается вместе с сервером, если задан TELEGRAM_BOT_TOKEN.

Каждый чат имеет свой набор документов. Управление кнопками:
  меню внизу — «Документы», «Кратко», «Очистить», «Помощь» (то же, что /docs, /summary, /clear, /start);
  после загрузки файла — краткое содержание и готовые вопросы кнопками;
  под каждым ответом — кнопки со следующими вопросами.
"""
import asyncio
import html
import io
import logging
import re
import secrets
from collections import OrderedDict

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ChatAction, ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import (CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, Message,
                           ReplyKeyboardMarkup)

from . import rag
from .auth import AuthError, limiter
from .config import settings
from .guard import is_junk
from .parsers import UnsupportedFormat
from .store import store

log = logging.getLogger(__name__)
dp = Dispatcher()

TEXTS = {
    "start": {
        "kk": "Сәлем! Мен <b>Mind AI</b> — құжаттар бойынша сұрақтарға жауап беретін чат-ботпын.\n\n"
              "1️⃣ Маған PDF, DOCX, PPTX, XLSX, TXT файлын немесе құжаттың фотосын жіберіңіз.\n"
              "2️⃣ Құжат бойынша сұрақ қойыңыз — қазақша, орысша немесе ағылшынша.\n"
              "3️⃣ Мен жауап беремін және дереккөзін (бетін) көрсетемін.\n\n"
              "Төмендегі батырмалар: 📄 құжаттар, 📝 қысқаша мазмұны, 🗑 тазалау.",
        "ru": "Привет! Я <b>Mind AI</b> — чат-бот, который отвечает на вопросы по вашим документам.\n\n"
              "1️⃣ Отправьте мне файл PDF, DOCX, PPTX, XLSX, TXT или фото документа.\n"
              "2️⃣ Задайте вопрос по документу — на казахском, русском или английском.\n"
              "3️⃣ Я отвечу и укажу источник (страницу).\n\n"
              "Кнопки внизу: 📄 документы, 📝 краткое содержание, 🗑 очистить.",
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
    "junk": {"kk": "🤔 Бұл құжат бойынша сұраққа ұқсамайды. Не білгіңіз келетінін жазыңыз — мысалы: «Қандай мерзімдер көрсетілген?»",
             "ru": "🤔 Похоже, это не вопрос по документу. Напишите, что хотите узнать, — например: «Какие сроки указаны?»"},
    "too_many": {"kk": "⏳ Сұраулар тым көп — сәл күте тұрыңыз.", "ru": "⏳ Слишком много запросов — подождите немного."},
    "ask_these": {"kk": "💡 Мынадай сұрақ қоюға болады:", "ru": "💡 Можно спросить:"},
    "clear_ask": {"kk": "Барлық құжаттар мен тарихты өшіру керек пе?", "ru": "Удалить все документы и историю?"},
    "yes_clear": {"kk": "✅ Иә, өшіру", "ru": "✅ Да, удалить"},
    "cancel": {"kk": "Болдырмау", "ru": "Отмена"},
    "cancelled": {"kk": "Жарайды, ештеңе өшірілмеді.", "ru": "Хорошо, ничего не удалено."},
    "placeholder": {"kk": "Құжат бойынша сұрақ қойыңыз…", "ru": "Задайте вопрос по документу…"},
}

# Кнопки меню внизу экрана: текст кнопки → действие
MENU = {
    "docs": {"kk": "📄 Құжаттар", "ru": "📄 Документы"},
    "summary": {"kk": "📝 Қысқаша", "ru": "📝 Кратко"},
    "clear": {"kk": "🗑 Тазалау", "ru": "🗑 Очистить"},
    "help": {"kk": "❓ Көмек", "ru": "❓ Помощь"},
}
MENU_ACTIONS = {text: action for action, variants in MENU.items() for text in variants.values()}


def menu_kb(lang: str) -> ReplyKeyboardMarkup:
    b = lambda key: KeyboardButton(text=MENU[key][lang])  # noqa: E731
    return ReplyKeyboardMarkup(keyboard=[[b("docs"), b("summary")], [b("clear"), b("help")]],
                               resize_keyboard=True, is_persistent=True, input_field_placeholder=tr("placeholder", lang))


# В callback_data Telegram помещается только 64 байта — сам текст вопроса храним здесь, в кнопке — его номер
_questions: OrderedDict[str, str] = OrderedDict()


def questions_kb(questions: list[str]) -> InlineKeyboardMarkup | None:
    rows = []
    for q in questions[:4]:
        key = secrets.token_hex(4)
        _questions[key] = q
        rows.append([InlineKeyboardButton(text=f"❓ {q}", callback_data=f"q:{key}")])
    while len(_questions) > 5000:
        _questions.popitem(last=False)
    return InlineKeyboardMarkup(inline_keyboard=rows) if rows else None


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


async def send_long(message: Message, text: str, reply_markup=None) -> Message | None:
    """Длинный текст — несколькими сообщениями; кнопки — под последним. Возвращает последнее сообщение."""
    last = None
    while text:
        part = text[:4000]
        if len(text) > 4000 and "\n" in part:
            part = part[: part.rfind("\n")]
        text = text[len(part):].lstrip()
        markup = reply_markup if not text else None
        try:
            last = await message.answer(part, reply_markup=markup)
        except Exception:  # noqa: BLE001 — если HTML сломался, отправляем как есть
            last = await message.answer(re.sub(r"<[^>]+>", "", part), parse_mode=None, reply_markup=markup)
    return last


@dp.message(CommandStart())
async def cmd_start(message: Message):
    lang = ui_lang(message)
    await message.answer(tr("start", lang), reply_markup=menu_kb(lang))


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
    lang = ui_lang(message)
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=tr("yes_clear", lang), callback_data="clear:yes"),
                                                InlineKeyboardButton(text=tr("cancel", lang), callback_data="clear:no")]])
    await message.answer(tr("clear_ask", lang), reply_markup=kb)


@dp.callback_query(F.data.startswith("clear:"))
async def on_clear(callback: CallbackQuery):
    lang = "kk" if (callback.from_user.language_code or "").startswith("kk") else "ru"
    if callback.data == "clear:yes":
        store.delete_owner(owner(callback.message))
        rag.history.clear(owner(callback.message))
        await callback.message.edit_text(tr("cleared", lang))
    else:
        await callback.message.edit_text(tr("cancelled", lang))
    await callback.answer()


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
    await send_long(message, f"📄 <b>{html.escape(doc['name'])}</b>\n\n{html.escape(result['summary'])}\n\n{tr('ask_these', lang)}",
                    reply_markup=questions_kb(result.get("questions", [])))


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
    # сразу — о чём документ и готовые вопросы кнопками: не нужно придумывать, что спросить
    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    try:
        result = await rag.summarize(doc, lang)
    except Exception:  # noqa: BLE001 — без резюме бот всё равно работает
        log.exception("Резюме для Telegram не удалось")
        return
    await send_long(message, f"📝 {html.escape(result['summary'])}\n\n{tr('ask_these', lang)}",
                    reply_markup=questions_kb(result.get("questions", [])))


@dp.message(F.document)
async def on_document(message: Message):
    doc = message.document
    await _ingest(message, doc.file_name or "document", doc.file_id, doc.file_size)


@dp.message(F.photo)
async def on_photo(message: Message):
    photo = message.photo[-1]  # самое большое разрешение
    await _ingest(message, f"photo_{message.message_id}.jpg", photo.file_id, photo.file_size)


async def answer_question(message: Message, question: str, lang: str) -> None:
    """Ответ с источниками; когда готовы подсказки следующего вопроса — кнопки под ответом."""
    # как на сайте: бессмыслица не уходит в модель, частые запросы ограничены — бережём общий ключ API
    if is_junk(question):
        await message.answer(tr("junk", lang))
        return
    try:
        limiter.hit("ask", owner(message))
    except AuthError:
        await message.answer(tr("too_many", lang))
        return
    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    parts, sources, last = [], [], None
    async for event in rag.answer_stream(question, owner(message), owner(message), None, {}):
        if event["type"] == "sources":
            sources = event["sources"]
        elif event["type"] == "delta":
            parts.append(event["text"])
        elif event["type"] == "done":
            by_n = {s["n"]: s for s in sources}
            cited = [by_n[n] for n in event.get("cited", []) if n in by_n]
            text = md_to_html("".join(parts).strip())
            if cited:
                src_lang = event["lang"] if event["lang"] in ("kk", "ru") else "ru"
                lines = [f"[{s['n']}] {html.escape(s['doc_name'])}{html.escape(', ' + s['loc_label'] if s['loc_label'] else '')}"
                         for s in cited[:5]]
                text += f"\n\n📚 <b>{tr('sources', src_lang)}:</b>\n" + "\n".join(lines)
            last = await send_long(message, text)
        elif event["type"] == "followups" and last:
            try:
                await last.edit_reply_markup(reply_markup=questions_kb(event["items"]))
            except Exception:  # noqa: BLE001 — без кнопок ответ всё равно на месте
                log.warning("Не удалось добавить кнопки вопросов")


@dp.message(F.text.in_(MENU_ACTIONS))
async def on_menu(message: Message):
    action = MENU_ACTIONS[message.text]
    handler = {"docs": cmd_docs, "summary": cmd_summary, "clear": cmd_clear, "help": cmd_start}[action]
    await handler(message)


@dp.message(F.text)
async def on_question(message: Message):
    await answer_question(message, message.text, ui_lang(message))


@dp.callback_query(F.data.startswith("q:"))
async def on_question_button(callback: CallbackQuery):
    question = _questions.get(callback.data[2:])
    lang = "kk" if (callback.from_user.language_code or "").startswith("kk") else "ru"
    await callback.answer()
    if not question:  # кнопка из очень старого сообщения — бот перезапускался
        return
    await callback.message.answer(f"❓ <b>{html.escape(question)}</b>")
    await answer_question(callback.message, question, lang)


async def run_bot():
    bot = Bot(settings.telegram_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    try:
        await dp.start_polling(bot, handle_signals=False)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_bot())
