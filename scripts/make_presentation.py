"""Генерирует презентацию docs/Mind_AI_Presentation.pptx (16:9, с заметками докладчика).

Структура подогнана под критерии направления AIChatBots (п. 5.1.2 Ереже):
актуальность и сфера применения (40), качество работы с документами и точность (30),
функциональность (15), презентация (15). Слайдов о рынке и финансах нет — за них баллы не дают.

Запуск:  .venv/bin/python scripts/make_presentation.py
Картинки берутся из docs/deck/. Поля «Команда / Колледж / Руководитель» заполните своими данными.
"""
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parent.parent
DECK = ROOT / "docs" / "deck"
OUT = ROOT / "docs" / "Mind_AI_Presentation.pptx"
SITE = "chatbotai-production-51ae.up.railway.app"
REPO = "github.com/adiletpn/ChatBotAI"

BG = RGBColor(0xF4, 0xF4, 0xF1)
CARD = RGBColor(0xFF, 0xFF, 0xFF)
INK = RGBColor(0x2A, 0x2A, 0x2F)
DARK = RGBColor(0x14, 0x14, 0x17)
MUTED = RGBColor(0x6B, 0x6B, 0x73)
LINE = RGBColor(0xE2, 0xE2, 0xDC)
ACCENT = RGBColor(0x63, 0x66, 0xF1)
ACCENT_SOFT = RGBColor(0xEC, 0xEC, 0xFD)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT = "Arial"

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
W, H = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


# ---------------------------------------------------------------- примитивы

def fill(slide, color):
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = color


def text(slide, x, y, w, h, value, size=18, bold=False, color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=1.1):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, line in enumerate(value if isinstance(value, list) else [value]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        run = p.add_run()
        run.text = line
        run.font.size, run.font.bold, run.font.color.rgb, run.font.name = Pt(size), bold, color, FONT
    return box


def rich(slide, x, y, w, h, items, size=16, gap=10, color=INK):
    """Список «жирное — пояснение»."""
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap)
        head, _, tail = item.partition(" — ")
        r = p.add_run()
        r.text = head
        r.font.size, r.font.bold, r.font.color.rgb, r.font.name = Pt(size), bool(tail), color, FONT
        if tail:
            r2 = p.add_run()
            r2.text = " — " + tail
            r2.font.size, r2.font.color.rgb, r2.font.name = Pt(size), MUTED, FONT
    return box


def box(slide, x, y, w, h, color=CARD, line=LINE, radius=0.06, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    s = slide.shapes.add_shape(shape, x, y, w, h)
    s.fill.solid()
    s.fill.fore_color.rgb = color
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(0.75)
    s.shadow.inherit = False
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    return s


def picture(slide, name, x, y, w=None, h=None, border=True):
    path = DECK / name
    if w is not None and h is not None:  # вписываем с сохранением пропорций и центрируем
        iw, ih = Image.open(path).size
        scale = min(w / iw, h / ih)
        pw, ph = int(iw * scale), int(ih * scale)
        x, y, w, h = x + (w - pw) // 2, y + (h - ph) // 2, pw, ph
        pic = slide.shapes.add_picture(str(path), x, y, w, h)
    else:
        pic = slide.shapes.add_picture(str(path), x, y, w, h)
    if border:
        pic.line.color.rgb = LINE
        pic.line.width = Pt(0.75)
    return pic


def card(slide, x, y, w, h, num, title, body, title_size=17, body_size=13):
    box(slide, x, y, w, h)
    if num:
        dot = box(slide, x + Inches(0.25), y + Inches(0.25), Inches(0.42), Inches(0.42), color=ACCENT_SOFT, line=None, shape=MSO_SHAPE.OVAL)
        tf = dot.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        r = tf.paragraphs[0].add_run()
        r.text = num
        r.font.size, r.font.bold, r.font.color.rgb, r.font.name = Pt(13), True, ACCENT, FONT
    top = y + (Inches(0.85) if num else Inches(0.25))
    text(slide, x + Inches(0.25), top, w - Inches(0.5), Inches(0.5), title, size=title_size, bold=True)
    text(slide, x + Inches(0.25), top + Inches(0.45), w - Inches(0.5), h - (top - y) - Inches(0.55), body, size=body_size, color=MUTED, spacing=1.15)


def slide(title, kicker="", notes=""):
    s = prs.slides.add_slide(BLANK)
    fill(s, BG)
    if kicker:
        text(s, Inches(0.7), Inches(0.45), Inches(9), Inches(0.3), kicker.upper(), size=11, bold=True, color=ACCENT)
    text(s, Inches(0.7), Inches(0.72), Inches(11.5), Inches(0.8), title, size=30, bold=True)
    pic = s.shapes.add_picture(str(DECK / "wordmark_dark.png"), W - Inches(1.75), H - Inches(0.6), height=Inches(0.28))
    pic.line.fill.background()
    text(s, Inches(0.7), H - Inches(0.55), Inches(2), Inches(0.3), str(len(prs.slides)), size=10, color=MUTED)
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s


# ---------------------------------------------------------------- 1. Введение

s = prs.slides.add_slide(BLANK)
fill(s, DARK)
s.shapes.add_picture(str(DECK / "wordmark_white.png"), Inches(0.8), Inches(1.3), height=Inches(1.15))
text(s, Inches(0.8), Inches(2.8), Inches(5.9), Inches(1.4),
     ["Интеллектуальный ассистент,", "который отвечает по документам"], size=24, bold=True, color=WHITE, spacing=1.15)
text(s, Inches(0.8), Inches(3.95), Inches(5.9), Inches(0.4), "Направление AIChatBots · Innovation AI Hackathon – 2026", size=14,
     color=RGBColor(0xA9, 0xAB, 0xF8))
text(s, Inches(0.8), Inches(5.3), Inches(5.5), Inches(1.4),
     ["Команда: ____________", "Колледж: ____________", "Руководитель: ____________"], size=14,
     color=RGBColor(0xC8, 0xC8, 0xCE), spacing=1.4)
picture(s, "chat.png", Inches(6.9), Inches(1.05), w=Inches(5.9), h=Inches(5.4), border=False)
s.notes_slide.notes_text_frame.text = (
    "Здравствуйте! Мы команда ___ из ___. Наш проект — Mind AI: интеллектуальный ассистент, который читает "
    "ваши документы и отвечает на вопросы по ним на казахском, русском и английском, всегда показывая источник.")

# ---------------------------------------------------------------- 2. Проблема

s = slide("Найти ответ в документе — долго и сложно", "Проблема",
          "Каждый из нас сталкивался: нужен один пункт из длинного документа. Его ищут вручную, документ может быть "
          "на другом языке или вообще сканом. А если ответ дал ИИ — непонятно, можно ли ему верить.")
problems = [("1", "Долгий поиск", "Положения, инструкции, учебные материалы занимают десятки страниц — нужный пункт ищут вручную."),
            ("2", "Разные языки и сканы", "Документ на казахском, вопрос на русском. Сканы и фото вообще не находятся обычным поиском."),
            ("3", "Нет доверия к ответу", "Ответ без указания источника нельзя проверить — а в учёбе и на работе ошибка дорого стоит.")]
for i, (n, t, b) in enumerate(problems):
    card(s, Inches(0.7) + i * Inches(4.05), Inches(1.95), Inches(3.8), Inches(3.3), n, t, b, title_size=19, body_size=15)
text(s, Inches(0.7), Inches(5.65), Inches(12), Inches(0.6),
     "Mind AI решает все три: быстро, на любом из трёх языков и с доказательством из документа.", size=17, bold=True, color=ACCENT)

# ---------------------------------------------------------------- 3. Решение

s = slide("Решение: загрузите документ — и задайте вопрос", "Решение",
          "Работа в три шага. Главное — каждый ответ подтверждён ссылкой на документ и страницу.")
steps = [("1", "Загрузите документ", "PDF, DOCX, PPTX, XLSX, TXT, скан или фото — на сайте или в Telegram"),
         ("2", "Задайте вопрос", "На казахском, русском или английском — текстом или голосом"),
         ("3", "Получите ответ с источником", "Точный ответ по документу и ссылки [1] [2] на страницу с цитатой")]
for i, (n, t, b) in enumerate(steps):
    y = Inches(1.85) + i * Inches(1.55)
    card(s, Inches(0.7), y, Inches(4.9), Inches(1.35), "", "", "")
    dot = box(s, Inches(0.95), y + Inches(0.4), Inches(0.55), Inches(0.55), color=ACCENT, line=None, shape=MSO_SHAPE.OVAL)
    tf = dot.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    r = tf.paragraphs[0].add_run()
    r.text = n
    r.font.size, r.font.bold, r.font.color.rgb, r.font.name = Pt(18), True, WHITE, FONT
    text(s, Inches(1.75), y + Inches(0.25), Inches(3.7), Inches(0.4), t, size=17, bold=True)
    text(s, Inches(1.75), y + Inches(0.68), Inches(3.7), Inches(0.6), b, size=12.5, color=MUTED)
picture(s, "chat.png", Inches(5.95), Inches(1.75), w=Inches(6.7), h=Inches(4.6))

# ---------------------------------------------------------------- 4. Как это работает

s = slide("Как это работает: технология RAG", "Технология",
          "RAG — Retrieval-Augmented Generation. Модель не «вспоминает», а читает найденные фрагменты документа. "
          "Поэтому ответы точные, а каждый факт подтверждён ссылкой.")
pipe = [("Чтение", "PDF, DOCX, PPTX, XLSX…\nсканы → OCR kaz/rus/eng"), ("Фрагменты", "текст делится на части\nс номером страницы"),
        ("Поиск", "BM25 + казахская и русская\nморфология, перевод ×3"), ("Ответ ИИ", "только по найденному\nтексту, без выдумок"),
        ("Источник", "ссылки [n], страница\nи подсветка строк")]
bw, gap = Inches(2.22), Inches(0.24)
for i, (t, b) in enumerate(pipe):
    x = Inches(0.7) + i * (bw + gap)
    box(s, x, Inches(1.95), bw, Inches(1.9), color=ACCENT_SOFT if i in (2, 3) else CARD)
    text(s, x, Inches(2.2), bw, Inches(0.4), t, size=17, bold=True, align=PP_ALIGN.CENTER, color=ACCENT if i in (2, 3) else INK)
    text(s, x + Inches(0.1), Inches(2.75), bw - Inches(0.2), Inches(0.9), b, size=12.5, color=MUTED, align=PP_ALIGN.CENTER)
    if i < len(pipe) - 1:
        a = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x + bw + Inches(0.03), Inches(2.78), Inches(0.18), Inches(0.24))
        a.fill.solid()
        a.fill.fore_color.rgb = ACCENT
        a.line.fill.background()
rich(s, Inches(0.7), Inches(4.35), Inches(11.9), Inches(2.2), [
    "Межъязыковой поиск — вопрос на русском находит ответ в казахском документе",
    "Только по документу — если ответа нет, Mind AI честно говорит об этом",
    "Работает и без связи с моделью — показывает найденные фрагменты с источниками",
], size=16)

# ---------------------------------------------------------------- 5. Продукт: доказательство

s = slide("Каждый ответ можно проверить за секунду", "Продукт · ответ с доказательством",
          "Нажимаем на источник под ответом — открывается настоящая страница документа, а строки, на которых основан "
          "ответ, подсвечены маркером. Под ответом — индикатор «подтверждено N источниками».")
picture(s, "evidence.png", Inches(0.7), Inches(1.75), w=Inches(7.6), h=Inches(4.9))
rich(s, Inches(8.65), Inches(1.95), Inches(4.0), Inches(4.6), [
    "Ссылки [1] [2] — у каждого факта в ответе",
    "Страница документа — открывается рядом с чатом",
    "Подсветка — именно те строки, на которых основан ответ",
    "Индикатор доверия — «подтверждено N источниками»",
], size=15, gap=14)

# ---------------------------------------------------------------- 6. Продукт: карта и тест

s = slide("Карта документа и проверка знаний", "Продукт · режимы",
          "Карта документа: ИИ сам раскладывает документ на сроки, цифры, требования и термины. "
          "Проверка знаний: тест по документу с объяснениями — например, после инструктажа по охране труда.")
picture(s, "map.png", Inches(0.7), Inches(1.75), w=Inches(5.95), h=Inches(3.72))
picture(s, "quiz.png", Inches(6.7), Inches(1.75), w=Inches(5.95), h=Inches(3.72))
text(s, Inches(0.7), Inches(5.6), Inches(5.9), Inches(0.4), "Карта документа", size=16, bold=True)
text(s, Inches(0.7), Inches(5.98), Inches(5.9), Inches(0.8), "Сроки, ключевые цифры, чек-лист требований и термины — без единого вопроса, каждый пункт со ссылкой на страницу.", size=12.5, color=MUTED)
text(s, Inches(6.7), Inches(5.6), Inches(5.9), Inches(0.4), "Проверка знаний", size=16, bold=True)
text(s, Inches(6.7), Inches(5.98), Inches(5.9), Inches(0.8), "Тест по документу: варианты ответа, мгновенная проверка, объяснение со ссылкой, итоговый балл и разбор ошибок.", size=12.5, color=MUTED)

# ---------------------------------------------------------------- 7. Продукт: платформа

s = slide("Готовая платформа, а не прототип", "Продукт · платформа",
          "Это полноценный сервис: аккаунты с подтверждением почты, сохранённые чаты, настройки, темы, мобильная версия. "
          "Он уже работает в интернете.")
picture(s, "settings.png", Inches(0.7), Inches(1.75), w=Inches(6.6), h=Inches(4.15))
picture(s, "mobile.png", Inches(7.55), Inches(1.75), w=Inches(2.05), h=Inches(4.45))
rich(s, Inches(9.95), Inches(1.85), Inches(2.75), Inches(4.8), [
    "Аккаунты — вход по email с кодом, сброс пароля",
    "Сохранённые чаты — история и контекст",
    "Настройки — 5 тем, 6 цветов, язык, стиль ответа",
    "Телефон — удобная мобильная версия",
    "Telegram — тот же бот в мессенджере",
], size=12.5, gap=10)

# ---------------------------------------------------------------- 8. Соответствие регламенту

s = slide("Все требования регламента выполнены", "Соответствие п. 5.1.2",
          "Пройдёмся по требованиям направления AIChatBots: всё выполнено, включая три дополнительные возможности.")
rows = [("Требование", "Как выполнено в Mind AI"),
        ("Работа с PDF, DOCX и другими документами", "10+ форматов: PDF, DOCX, PPTX, XLSX, CSV, TXT, HTML, сканы и фото"),
        ("Точные и понятные ответы по содержанию", "RAG + запрет выдумывать + ссылка на страницу у каждого факта"),
        ("Технологии ИИ и обработки языка (NLP)", "Языковая модель, определение языка, морфология kk/ru, перевод запроса"),
        ("Telegram, WhatsApp или веб-платформа", "Веб-платформа и Telegram-бот"),
        ("Рабочая версия", f"Работает онлайн: {SITE}"),
        ("★ Указание источника", "Ссылки [n], страница документа и подсветка строк"),
        ("★ Многоязычие", "Вопросы, ответы и интерфейс на казахском, русском, английском"),
        ("★ Сканированные документы", "OCR с казахской, русской и английской моделями")]
tbl = s.shapes.add_table(len(rows), 2, Inches(0.7), Inches(1.75), Inches(11.9), Inches(4.9)).table
tbl.columns[0].width, tbl.columns[1].width = Inches(4.6), Inches(7.3)
for r, (a, b) in enumerate(rows):
    for c, value in enumerate((a, b)):
        cell = tbl.cell(r, c)
        cell.text = value
        para = cell.text_frame.paragraphs[0]
        run = para.runs[0]
        run.font.size, run.font.name = Pt(13.5), FONT
        run.font.bold = r == 0 or c == 0
        run.font.color.rgb = WHITE if r == 0 else (ACCENT if a.startswith("★") and c == 0 else INK)
        cell.fill.solid()
        cell.fill.fore_color.rgb = INK if r == 0 else (CARD if r % 2 else BG)
        cell.margin_left = cell.margin_right = Inches(0.15)

# ---------------------------------------------------------------- 9. Результаты

s = slide("Результаты: работает, проверено, онлайн", "Результаты",
          "Продукт проверен автотестами и на реальных документах. Он уже доступен по ссылке — можно открыть прямо сейчас.")
stats = [("10+", "форматов документов"), ("3", "языка: kk · ru · en"), ("52", "автоматические проверки"),
         ("~10 с", "на ответ с источниками"), ("24/7", "работает онлайн"), ("3", "режима: чат · карта · тест")]
for i, (v, l) in enumerate(stats):
    col, row = i % 3, i // 3
    x, y = Inches(0.7) + col * Inches(4.05), Inches(1.85) + row * Inches(1.75)
    box(s, x, y, Inches(3.8), Inches(1.5))
    text(s, x + Inches(0.3), y + Inches(0.22), Inches(3.3), Inches(0.7), v, size=34, bold=True, color=ACCENT)
    text(s, x + Inches(0.3), y + Inches(0.95), Inches(3.3), Inches(0.4), l, size=14, color=MUTED)
text(s, Inches(0.7), Inches(5.55), Inches(12), Inches(0.9),
     ["Проверено: вопрос на русском к казахскому документу, ответы по сканам, честное «в документе этого нет»,",
      "регистрация с кодом, сброс пароля и изоляция данных пользователей."], size=14, color=MUTED, spacing=1.25)

# ---------------------------------------------------------------- 10. Чем Mind AI особенный

s = slide("Что делает Mind AI особенным", "Уникальность",
          "Шесть вещей, которые делают Mind AI особенным: доказательство на странице, казахский язык, режимы помимо чата, "
          "честность, приватность и работа даже без связи с моделью.")
feats = [("Доказательство на странице", "Ответ подтверждён подсвеченными строками в самом документе."),
         ("Казахский язык", "Морфология в поиске, OCR казахских сканов, интерфейс на трёх языках."),
         ("Больше, чем чат", "Карта документа и проверка знаний — без единого вопроса."),
         ("Честность", "Если ответа нет в документе, Mind AI так и говорит — без выдумок."),
         ("Приватность", "Каждый пользователь видит только свои документы и чаты."),
         ("Надёжность", "Без связи с моделью продолжает находить фрагменты с источниками.")]
for i, (t, b) in enumerate(feats):
    col, row = i % 3, i // 3
    card(s, Inches(0.7) + col * Inches(4.05), Inches(1.85) + row * Inches(2.3), Inches(3.8), Inches(2.05), str(i + 1), t, b,
         title_size=16, body_size=13)

# ---------------------------------------------------------------- 11. Где применять

s = slide("Где применять Mind AI", "Сфера применения",
          "Mind AI подходит для любой организации, где много документов: колледжи, предприятия, госорганы, бизнес.")
uses = [("Образование", "Учебники, методички, положения и правила — помощник для студентов и преподавателей."),
        ("Производство и охрана труда", "Инструкции, регламенты, нормы СИЗ — быстрый ответ рабочему и проверка знаний после инструктажа."),
        ("Госсектор", "Приказы, законы, стандарты — поиск по документам на казахском и русском."),
        ("Бизнес и юристы", "Договоры, политики, отчёты — ответы с точной ссылкой на пункт и страницу.")]
for i, (t, b) in enumerate(uses):
    col, row = i % 2, i // 2
    card(s, Inches(0.7) + col * Inches(6.05), Inches(1.85) + row * Inches(2.3), Inches(5.85), Inches(2.05), str(i + 1), t, b,
         title_size=18, body_size=14)

# ---------------------------------------------------------------- 12. Команда

s = slide("Команда", "Команда", "Представьте участников команды и их роли.")
for i in range(3):
    x = Inches(0.7) + i * Inches(4.05)
    box(s, x, Inches(1.95), Inches(3.8), Inches(3.4))
    box(s, x + Inches(1.35), Inches(2.3), Inches(1.1), Inches(1.1), color=ACCENT_SOFT, line=None, shape=MSO_SHAPE.OVAL)
    text(s, x, Inches(3.65), Inches(3.8), Inches(0.4), "Имя Фамилия", size=17, bold=True, align=PP_ALIGN.CENTER)
    text(s, x + Inches(0.3), Inches(4.1), Inches(3.2), Inches(0.9), "Роль в проекте", size=13, color=MUTED, align=PP_ALIGN.CENTER)
text(s, Inches(0.7), Inches(5.75), Inches(12), Inches(0.4), "Руководитель: ____________", size=15, color=MUTED)

# ---------------------------------------------------------------- 13. Что дальше

s = slide("Что дальше", "Развитие",
          "Планы развития: WhatsApp, вход через Google, семантический поиск, голосовые ответы на казахском, "
          "общие базы знаний для организаций.")
plan = [("WhatsApp-бот", "ещё один привычный мессенджер"), ("Вход через Google", "регистрация в один клик"),
        ("Семантический поиск", "поиск по смыслу, а не только по словам"), ("Голосовые ответы", "озвучивание ответов на казахском"),
        ("Базы знаний организаций", "общие документы для команды или колледжа")]
for i, (t, b) in enumerate(plan):
    y = Inches(1.9) + i * Inches(0.92)
    dot = box(s, Inches(0.7), y + Inches(0.08), Inches(0.42), Inches(0.42), color=ACCENT, line=None, shape=MSO_SHAPE.OVAL)
    tf = dot.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    r = tf.paragraphs[0].add_run()
    r.text = str(i + 1)
    r.font.size, r.font.bold, r.font.color.rgb, r.font.name = Pt(13), True, WHITE, FONT
    text(s, Inches(1.35), y + Inches(0.06), Inches(4.5), Inches(0.45), t, size=18, bold=True)
    text(s, Inches(5.2), y + Inches(0.1), Inches(7.4), Inches(0.45), b, size=15, color=MUTED)

# ---------------------------------------------------------------- 14. Спасибо

s = prs.slides.add_slide(BLANK)
fill(s, DARK)
s.shapes.add_picture(str(DECK / "wordmark_white.png"), Inches(0.8), Inches(1.6), height=Inches(1.0))
text(s, Inches(0.8), Inches(2.95), Inches(7.5), Inches(0.8), "Рахмет! Спасибо!", size=40, bold=True, color=WHITE)
text(s, Inches(0.8), Inches(3.85), Inches(7.5), Inches(0.5), "Попробуйте Mind AI прямо сейчас", size=18, color=RGBColor(0xC8, 0xC8, 0xCE))
text(s, Inches(0.8), Inches(4.75), Inches(7.5), Inches(1.2), [SITE, REPO], size=15, color=RGBColor(0xA9, 0xAB, 0xF8), spacing=1.5)
box(s, Inches(9.0), Inches(1.6), Inches(3.4), Inches(3.4), color=WHITE, line=None, radius=0.08)
s.shapes.add_picture(str(DECK / "qr_site.png"), Inches(9.25), Inches(1.85), Inches(2.9), Inches(2.9))
text(s, Inches(9.0), Inches(5.2), Inches(3.4), Inches(0.4), "Сканируйте, чтобы открыть", size=13, color=RGBColor(0xC8, 0xC8, 0xCE), align=PP_ALIGN.CENTER)
s.notes_slide.notes_text_frame.text = "Спасибо за внимание! Mind AI уже работает онлайн — откройте по QR-коду. Готовы ответить на вопросы."

prs.save(OUT)
print("saved", OUT, f"({len(prs.slides)} слайдов)")
