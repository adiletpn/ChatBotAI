"use strict";

/* ================= i18n ================= */
const I18N = {
  kk: {
    tagline: "Құжаттар бойынша зияткер көмекші",
    upload_title: "Құжатты жүктеу",
    documents: "Құжаттар",
    no_docs_hint: "Файлды осында сүйреңіз немесе жоғарыдағы аймақты басыңыз",
    clear_chat: "Чатты тазалау",
    welcome_title: "Құжатыңызбен <span class=\"grad\">сөйлесіңіз</span>",
    welcome_text: "Кез келген құжатты жүктеңіз — Mind AI оның мазмұны бойынша сұрақтарға нақты жауап беріп, дереккөзін көрсетеді.",
    f1_t: "Кез келген формат", f1_d: "PDF, DOCX, PPTX, XLSX, TXT, HTML, суреттер",
    f2_t: "Дереккөзді көрсету", f2_d: "Әр жауапта құжат пен бет нөмірі",
    f3_t: "Үш тіл", f3_d: "Қазақша, орысша, ағылшынша сұрақ қойыңыз",
    f4_t: "Сканерлер (OCR)", f4_d: "Сканерленген құжаттар мен фотоларды оқиды",
    step1: "Құжатты жүктеңіз", step2: "Сұрақ қойыңыз", step3: "Дереккөзімен жауап алыңыз",
    placeholder: "Құжат бойынша сұрақ қойыңыз…",
    voice: "Дауыспен сұрау",
    disclaimer: "Жауаптар тек жүктелген құжаттар негізінде құрылады. Маңызды ақпаратты дереккөзден тексеріңіз.",
    scope_all: "Барлық құжаттар бойынша іздеу",
    scope_sel: "Таңдалған құжаттар:",
    pages: "бет", chunks: "фрагмент", ocr: "OCR",
    summary: "Қысқаша", open: "Ашу", delete: "Өшіру",
    uploading: "Өңделуде…",
    uploaded: "жүктелді",
    upload_error: "Қате",
    sources: "Дереккөздер",
    copy: "Көшіру", copied: "Көшірілді",
    open_doc: "Құжатты ашу",
    llm_on: "AI моделі", llm_off: "Офлайн режим (LLM жоқ)",
    ocr_on: "OCR", ocr_off: "OCR өшірулі",
    tg: "Telegram-бот қосулы",
    confirm_delete: "Құжатты өшіру керек пе?",
    cleared: "Чат тазаланды",
    doc_ready: "Құжат дайын",
    summary_title: "Қысқаша мазмұны",
    ask_these: "Мына сұрақтарды қойып көріңіз:",
    error: "Қате орын алды",
  },
  ru: {
    tagline: "Интеллектуальный помощник по документам",
    upload_title: "Загрузить документ",
    documents: "Документы",
    no_docs_hint: "Перетащите файл сюда или нажмите на область выше",
    clear_chat: "Очистить чат",
    welcome_title: "Поговорите со своим <span class=\"grad\">документом</span>",
    welcome_text: "Загрузите любой документ — Mind AI ответит на вопросы по его содержанию и покажет точный источник.",
    f1_t: "Любой формат", f1_d: "PDF, DOCX, PPTX, XLSX, TXT, HTML, изображения",
    f2_t: "Указание источника", f2_d: "В каждом ответе — документ и номер страницы",
    f3_t: "Три языка", f3_d: "Спрашивайте на казахском, русском, английском",
    f4_t: "Сканы (OCR)", f4_d: "Читает сканированные документы и фото",
    step1: "Загрузите документ", step2: "Задайте вопрос", step3: "Получите ответ с источником",
    placeholder: "Задайте вопрос по документу…",
    voice: "Голосовой вопрос",
    disclaimer: "Ответы формируются только на основе загруженных документов. Проверяйте важные данные по источнику.",
    scope_all: "Поиск по всем документам",
    scope_sel: "Выбранные документы:",
    pages: "стр.", chunks: "фрагм.", ocr: "OCR",
    summary: "Кратко", open: "Открыть", delete: "Удалить",
    uploading: "Обработка…",
    uploaded: "загружен",
    upload_error: "Ошибка",
    sources: "Источники",
    copy: "Копировать", copied: "Скопировано",
    open_doc: "Открыть документ",
    llm_on: "AI-модель", llm_off: "Офлайн-режим (без LLM)",
    ocr_on: "OCR", ocr_off: "OCR отключён",
    tg: "Telegram-бот подключён",
    confirm_delete: "Удалить документ?",
    cleared: "Чат очищен",
    doc_ready: "Документ готов",
    summary_title: "Краткое содержание",
    ask_these: "Попробуйте спросить:",
    error: "Произошла ошибка",
  },
  en: {
    tagline: "Intelligent document assistant",
    upload_title: "Upload document",
    documents: "Documents",
    no_docs_hint: "Drop a file here or click the area above",
    clear_chat: "Clear chat",
    welcome_title: "Chat with your <span class=\"grad\">documents</span>",
    welcome_text: "Upload any document — Mind AI answers questions about its content and shows the exact source.",
    f1_t: "Any format", f1_d: "PDF, DOCX, PPTX, XLSX, TXT, HTML, images",
    f2_t: "Source citations", f2_d: "Every answer shows the document and page",
    f3_t: "Three languages", f3_d: "Ask in Kazakh, Russian or English",
    f4_t: "Scans (OCR)", f4_d: "Reads scanned documents and photos",
    step1: "Upload a document", step2: "Ask a question", step3: "Get an answer with sources",
    placeholder: "Ask a question about your documents…",
    voice: "Voice question",
    disclaimer: "Answers are generated only from the uploaded documents. Verify important facts in the source.",
    scope_all: "Searching all documents",
    scope_sel: "Selected documents:",
    pages: "pp.", chunks: "chunks", ocr: "OCR",
    summary: "Summary", open: "Open", delete: "Delete",
    uploading: "Processing…",
    uploaded: "uploaded",
    upload_error: "Error",
    sources: "Sources",
    copy: "Copy", copied: "Copied",
    open_doc: "Open document",
    llm_on: "AI model", llm_off: "Offline mode (no LLM)",
    ocr_on: "OCR", ocr_off: "OCR disabled",
    tg: "Telegram bot connected",
    confirm_delete: "Delete this document?",
    cleared: "Chat cleared",
    doc_ready: "Document ready",
    summary_title: "Summary",
    ask_these: "Try asking:",
    error: "Something went wrong",
  },
};

Object.assign(I18N.kk, {
  tab_chat: "Сұрақ-жауап", tab_map: "Құжат картасы", tab_quiz: "Білімді тексеру",
  map_h: "Құжат картасы",
  map_sub: "AI құжатты өзі талдайды: мерзімдер, негізгі сандар, талаптар және терминдер — әрқайсысы бетке сілтемесімен.",
  quiz_h: "Білімді тексеру",
  quiz_sub: "Құжат бойынша тест пен карточкалар: оқу материалын, нұсқаулықты немесе кез келген құжатты қаншалықты меңгергеніңізді тексеріңіз.",
  timeline: "Хронология және мерзімдер", numbers: "Негізгі сандар", requirements: "Талаптар чек-парағы", terms: "Терминдер мен атаулар",
  nothing: "Табылмады", done_of: "орындалды", need_doc: "Құжатты жүктеу үшін басыңыз немесе файлды осында сүйреңіз", need_doc_t: "Құжат әлі жоқ",
  analyzing: "AI құжатты талдап жатыр…", generating: "Сұрақтар құрастырылуда…",
  quiz_intro: "Сұрақтар саны", quiz_start: "Тестті бастау", question: "Сұрақ", next: "Келесі →", finish: "Нәтижені көру",
  retry: "Қайта тапсыру", new_quiz: "Жаңа сұрақтар", correct: "Дұрыс!", wrong: "Қате",
  score_great: "Керемет! Құжатты жақсы білесіз", score_ok: "Жаман емес — бірақ қайталап шығыңыз", score_low: "Құжатты қайта оқып шығу керек",
  your_mistakes: "Қателерді талдау", correct_answer: "Дұрыс жауап", evidence: "Дәлел",
  trust_ok: "{n} дереккөзбен расталған", trust_none: "Құжатта дәлел табылмады",
  stat_pages: "бет", stat_dates: "мерзім", stat_numbers: "сан", stat_req: "талап", map_btn: "Карта",
  logout: "Шығу", llm_fail: "қосылмады", guest: "Қонақ режимі",
});
Object.assign(I18N.ru, {
  tab_chat: "Вопрос-ответ", tab_map: "Карта документа", tab_quiz: "Проверка знаний",
  map_h: "Карта документа",
  map_sub: "AI сам разбирает документ: сроки, ключевые цифры, требования и термины — каждый пункт со ссылкой на страницу.",
  quiz_h: "Проверка знаний",
  quiz_sub: "Тест и карточки по документу: проверьте и закрепите, насколько хорошо усвоен учебный материал, инструкция или любой другой документ.",
  timeline: "Хронология и сроки", numbers: "Ключевые цифры", requirements: "Чек-лист требований", terms: "Термины и понятия",
  nothing: "Не найдено", done_of: "выполнено", need_doc: "Нажмите, чтобы загрузить документ, или перетащите файл сюда", need_doc_t: "Пока нет документов",
  analyzing: "AI анализирует документ…", generating: "Составляю вопросы…",
  quiz_intro: "Количество вопросов", quiz_start: "Начать тест", question: "Вопрос", next: "Далее →", finish: "Показать результат",
  retry: "Пройти заново", new_quiz: "Новые вопросы", correct: "Верно!", wrong: "Неверно",
  score_great: "Отлично! Вы хорошо знаете документ", score_ok: "Неплохо — но стоит повторить", score_low: "Документ стоит перечитать",
  your_mistakes: "Разбор ошибок", correct_answer: "Правильный ответ", evidence: "Доказательство",
  trust_ok: "Подтверждено {n} источн.", trust_none: "Подтверждение в документе не найдено",
  stat_pages: "стр.", stat_dates: "сроков", stat_numbers: "цифр", stat_req: "требований", map_btn: "Карта",
  logout: "Выйти", llm_fail: "нет связи", guest: "Гостевой режим",
});
Object.assign(I18N.en, {
  tab_chat: "Q&A", tab_map: "Document map", tab_quiz: "Knowledge check",
  map_h: "Document map",
  map_sub: "AI breaks the document down for you: deadlines, key numbers, requirements and terms — each linked to its page.",
  quiz_h: "Knowledge check",
  quiz_sub: "A quiz and flashcards based on the document: check and reinforce how well study material, an instruction or any other document has been learned.",
  timeline: "Timeline & deadlines", numbers: "Key numbers", requirements: "Requirements checklist", terms: "Terms & names",
  nothing: "Nothing found", done_of: "done", need_doc: "Click to upload a document or drop a file here", need_doc_t: "No documents yet",
  analyzing: "AI is analyzing the document…", generating: "Generating questions…",
  quiz_intro: "Number of questions", quiz_start: "Start the test", question: "Question", next: "Next →", finish: "See result",
  retry: "Try again", new_quiz: "New questions", correct: "Correct!", wrong: "Wrong",
  score_great: "Excellent! You know this document well", score_ok: "Not bad — worth a review", score_low: "Better re-read the document",
  your_mistakes: "Review of mistakes", correct_answer: "Correct answer", evidence: "Evidence",
  trust_ok: "Backed by {n} source(s)", trust_none: "No supporting evidence found",
  stat_pages: "pages", stat_dates: "dates", stat_numbers: "numbers", stat_req: "requirements", map_btn: "Map",
  logout: "Log out", llm_fail: "unreachable", guest: "Guest mode",
});

Object.assign(I18N.kk, {"dz_hint": "PDF, DOCX, PPTX, XLSX, сурет", "settings": "Баптаулар", "set_profile": "Профиль", "set_appearance": "Сыртқы түрі", "set_language": "Тіл", "set_ai": "AI жауаптары", "set_data": "Деректер", "set_system": "Жүйе туралы", "set_account": "Аккаунт", "profile_sub": "Сіз туралы ақпарат", "name": "Аты", "email": "Email", "save": "Сақтау", "saved": "Сақталды", "guest_note": "Сіз қонақ режиміндесіз. Деректерді сақтау үшін тіркеліңіз.", "appearance_sub": "Интерфейсті өзіңізге ыңғайлы етіңіз", "theme": "Тақырып", "theme_system": "Жүйелік", "theme_light": "Жарық", "theme_dark": "Қараңғы", "font_size": "Мәтін өлшемі", "font_size_d": "Барлық интерфейс үшін", "f_s": "Кіші", "f_m": "Орташа", "f_l": "Үлкен", "width": "Чат ені", "width_d": "Кең экрандар үшін", "w_normal": "Қалыпты", "w_wide": "Кең", "language_sub": "Бір баптау — бүкіл Mind AI үшін", "ui_lang": "Тіл", "ui_lang_d": "Мәзір, құжат картасы мен тесттер. Чатта бот сұрағыңыз қойылған тілде жауап береді", "answer_lang": "Жауап тілі", "answer_lang_d": "«Авто» — сұрақ қойылған тілде", "auto": "Авто", "ai_sub": "Mind AI қалай жауап береді", "style": "Жауап стилі", "style_d": "Жауап ұзындығы мен толықтығы", "st_concise": "Қысқа", "st_balanced": "Теңгерімді", "st_detailed": "Толық", "show_sources": "Дереккөздерді көрсету", "show_sources_d": "Жауап астындағы құжат пен бет сілтемелері", "show_trust": "Сенімділік белгісі", "show_trust_d": "«N дереккөзбен расталған»", "suggestions": "Сұрақ ұсыныстары", "suggestions_d": "Құжат жүктелгеннен кейін", "data_sub": "Құжаттар мен чат тарихы", "docs_count": "Жүктелген құжаттар", "export": "Чатты жүктеп алу", "export_d": "Бүкіл диалог .md файлына", "clear_hist": "Чат тарихын тазалау", "clear_hist_d": "Құжаттар сақталады", "delete_docs": "Барлық құжатты өшіру", "delete_docs_d": "Қайтару мүмкін емес", "confirm_all": "Барлық құжатты өшіру керек пе?", "done": "Дайын", "do_it": "Орындау", "system_sub": "Mind AI жұмысының техникалық күйі", "model": "AI моделі", "connected": "Қосулы", "disconnected": "Байланыс жоқ", "offline": "Офлайн режим", "check": "Тексеру", "checking": "Тексерілуде…", "ocr_card": "Сканерлерді тану", "ocr_none": "Қолжетімсіз", "telegram": "Telegram-бот", "tg_on": "Қосулы", "tg_off": "Қосылмаған", "formats": "Пішімдер", "version": "Нұсқа", "account_sub": "Қауіпсіздік және кіру", "change_pw": "Құпиясөзді өзгерту", "old_pw": "Ағымдағы құпиясөз", "new_pw": "Жаңа құпиясөз", "pw_rule": "Кемінде 8 таңба, әріптер мен сандар", "pw_changed": "Құпиясөз өзгертілді", "logout_d": "Осы құрылғыдан шығу", "danger": "Қауіпті аймақ", "delete_acc": "Аккаунтты өшіру", "delete_acc_d": "Барлық құжаттар мен деректер өшіріледі", "confirm_pw": "Растау үшін құпиясөзді енгізіңіз", "confirm_del": "Аккаунтты біржола өшіру керек пе?", "you": "Сіз", "llm_down": "AI моделімен байланыс жоқ — жауаптар офлайн режимде", "err_password_short": "Құпиясөз кемінде 8 таңба болуы керек", "err_password_weak": "Құпиясөзде әріптер мен сандар болуы керек", "err_invalid": "Құпиясөз қате", "err_name_invalid": "Атыңызды енгізіңіз"});
Object.assign(I18N.ru, {"dz_hint": "PDF, DOCX, PPTX, XLSX, фото", "settings": "Настройки", "set_profile": "Профиль", "set_appearance": "Внешний вид", "set_language": "Язык", "set_ai": "Ответы ИИ", "set_data": "Данные", "set_system": "О системе", "set_account": "Аккаунт", "profile_sub": "Информация о вас", "name": "Имя", "email": "Email", "save": "Сохранить", "saved": "Сохранено", "guest_note": "Вы в гостевом режиме. Зарегистрируйтесь, чтобы сохранить данные.", "appearance_sub": "Настройте интерфейс под себя", "theme": "Тема", "theme_system": "Системная", "theme_light": "Светлая", "theme_dark": "Тёмная", "font_size": "Размер текста", "font_size_d": "Для всего интерфейса", "f_s": "Мелкий", "f_m": "Средний", "f_l": "Крупный", "width": "Ширина чата", "width_d": "Для широких экранов", "w_normal": "Обычная", "w_wide": "Широкая", "language_sub": "Одна настройка — для всего Mind AI", "ui_lang": "Язык", "ui_lang_d": "Меню, карта документа и тесты. В чате бот отвечает на языке вашего вопроса", "answer_lang": "Язык ответов", "answer_lang_d": "«Авто» — на языке вопроса", "auto": "Авто", "ai_sub": "Как отвечает Mind AI", "style": "Стиль ответа", "style_d": "Длина и подробность ответов", "st_concise": "Кратко", "st_balanced": "Сбалансированно", "st_detailed": "Подробно", "show_sources": "Показывать источники", "show_sources_d": "Ссылки на документ и страницу под ответом", "show_trust": "Индикатор доверия", "show_trust_d": "«Подтверждено N источниками»", "suggestions": "Подсказки вопросов", "suggestions_d": "После загрузки документа", "data_sub": "Документы и история чата", "docs_count": "Загружено документов", "export": "Скачать чат", "export_d": "Весь диалог в файл .md", "clear_hist": "Очистить историю чата", "clear_hist_d": "Документы останутся", "delete_docs": "Удалить все документы", "delete_docs_d": "Действие нельзя отменить", "confirm_all": "Удалить все документы?", "done": "Готово", "do_it": "Выполнить", "system_sub": "Техническое состояние Mind AI", "model": "Модель ИИ", "connected": "Подключено", "disconnected": "Нет связи", "offline": "Офлайн-режим", "check": "Проверить", "checking": "Проверяю…", "ocr_card": "Распознавание сканов", "ocr_none": "Недоступно", "telegram": "Telegram-бот", "tg_on": "Подключён", "tg_off": "Не подключён", "formats": "Форматы", "version": "Версия", "account_sub": "Безопасность и вход", "change_pw": "Смена пароля", "old_pw": "Текущий пароль", "new_pw": "Новый пароль", "pw_rule": "Минимум 8 символов, буквы и цифры", "pw_changed": "Пароль изменён", "logout_d": "Выйти на этом устройстве", "danger": "Опасная зона", "delete_acc": "Удалить аккаунт", "delete_acc_d": "Все документы и данные будут удалены", "confirm_pw": "Введите пароль для подтверждения", "confirm_del": "Удалить аккаунт навсегда?", "you": "Вы", "llm_down": "Нет связи с моделью ИИ — ответы в офлайн-режиме", "err_password_short": "Пароль должен быть не короче 8 символов", "err_password_weak": "В пароле должны быть буквы и цифры", "err_invalid": "Неверный пароль", "err_name_invalid": "Введите имя"});
Object.assign(I18N.en, {"dz_hint": "PDF, DOCX, PPTX, XLSX, photo", "settings": "Settings", "set_profile": "Profile", "set_appearance": "Appearance", "set_language": "Language", "set_ai": "AI answers", "set_data": "Data", "set_system": "System", "set_account": "Account", "profile_sub": "Information about you", "name": "Name", "email": "Email", "save": "Save", "saved": "Saved", "guest_note": "You are in guest mode. Sign up to keep your data.", "appearance_sub": "Make the interface yours", "theme": "Theme", "theme_system": "System", "theme_light": "Light", "theme_dark": "Dark", "font_size": "Text size", "font_size_d": "For the whole interface", "f_s": "Small", "f_m": "Medium", "f_l": "Large", "width": "Chat width", "width_d": "For wide screens", "w_normal": "Normal", "w_wide": "Wide", "language_sub": "One setting for all of Mind AI", "ui_lang": "Language", "ui_lang_d": "Menus, document map and quizzes. In chat the bot answers in the language of your question", "answer_lang": "Answer language", "answer_lang_d": "“Auto” — same as the question", "auto": "Auto", "ai_sub": "How Mind AI answers", "style": "Answer style", "style_d": "Length and level of detail", "st_concise": "Concise", "st_balanced": "Balanced", "st_detailed": "Detailed", "show_sources": "Show sources", "show_sources_d": "Document and page links under answers", "show_trust": "Trust indicator", "show_trust_d": "“Backed by N sources”", "suggestions": "Question suggestions", "suggestions_d": "After a document is uploaded", "data_sub": "Documents and chat history", "docs_count": "Documents uploaded", "export": "Download chat", "export_d": "The whole conversation as .md", "clear_hist": "Clear chat history", "clear_hist_d": "Documents are kept", "delete_docs": "Delete all documents", "delete_docs_d": "This cannot be undone", "confirm_all": "Delete all documents?", "done": "Done", "do_it": "Run", "system_sub": "Technical status of Mind AI", "model": "AI model", "connected": "Connected", "disconnected": "Unreachable", "offline": "Offline mode", "check": "Check", "checking": "Checking…", "ocr_card": "Scan recognition", "ocr_none": "Unavailable", "telegram": "Telegram bot", "tg_on": "Connected", "tg_off": "Not connected", "formats": "Formats", "version": "Version", "account_sub": "Security and sign-in", "change_pw": "Change password", "old_pw": "Current password", "new_pw": "New password", "pw_rule": "At least 8 characters, letters and digits", "pw_changed": "Password changed", "logout_d": "Sign out on this device", "danger": "Danger zone", "delete_acc": "Delete account", "delete_acc_d": "All documents and data will be deleted", "confirm_pw": "Enter your password to confirm", "confirm_del": "Delete your account forever?", "you": "You", "llm_down": "AI model unreachable — answers in offline mode", "err_password_short": "Password must be at least 8 characters", "err_password_weak": "Password must contain letters and digits", "err_invalid": "Wrong password", "err_name_invalid": "Enter your name"});

Object.assign(I18N.kk, {"theme_sepia": "Қағаз", "theme_midnight": "Түнгі", "accent": "Акцент түсі", "accent_d": "Батырмалар мен сілтемелер", "ac_graphite": "Графит", "ac_indigo": "Индиго", "ac_emerald": "Изумруд", "ac_ocean": "Мұхит", "ac_amber": "Янтарь", "ac_rose": "Раушан"});
Object.assign(I18N.ru, {"theme_sepia": "Бумага", "theme_midnight": "Полночь", "accent": "Акцентный цвет", "accent_d": "Кнопки и ссылки", "ac_graphite": "Графит", "ac_indigo": "Индиго", "ac_emerald": "Изумруд", "ac_ocean": "Океан", "ac_amber": "Янтарь", "ac_rose": "Роза"});
Object.assign(I18N.en, {"theme_sepia": "Paper", "theme_midnight": "Midnight", "accent": "Accent color", "accent_d": "Buttons and links", "ac_graphite": "Graphite", "ac_indigo": "Indigo", "ac_emerald": "Emerald", "ac_ocean": "Ocean", "ac_amber": "Amber", "ac_rose": "Rose"});

Object.assign(I18N.kk, {"chats": "Чаттар", "new_chat": "Жаңа чат", "no_chats": "Чаттар әлі жоқ — сұрақ қойыңыз", "cancel": "Болдырмау", "del_chat_t": "Чатты өшіру керек пе?", "del_chat_d": "«{t}» чаты біржола өшіріледі.", "del_doc_t": "Құжатты өшіру керек пе?", "del_doc_d": "«{t}» және оның барлық фрагменттері өшіріледі.", "del_all_docs_t": "Барлық құжатты өшіру керек пе?", "del_all_chats_t": "Барлық чатты өшіру керек пе?", "irreversible": "Бұл әрекетті қайтару мүмкін емес.", "del_acc_t": "Аккаунтты өшіру керек пе?", "clear_hist": "Барлық чатты өшіру", "clear_hist_d": "Құжаттар сақталады", "chat_deleted": "Чат өшірілді", "untitled": "Жаңа чат"});
Object.assign(I18N.ru, {"chats": "Чаты", "new_chat": "Новый чат", "no_chats": "Чатов пока нет — задайте вопрос", "cancel": "Отмена", "del_chat_t": "Удалить этот чат?", "del_chat_d": "Чат «{t}» будет удалён без возможности восстановления.", "del_doc_t": "Удалить документ?", "del_doc_d": "«{t}» и все его фрагменты будут удалены.", "del_all_docs_t": "Удалить все документы?", "del_all_chats_t": "Удалить все чаты?", "irreversible": "Это действие нельзя отменить.", "del_acc_t": "Удалить аккаунт?", "clear_hist": "Удалить все чаты", "clear_hist_d": "Документы останутся", "chat_deleted": "Чат удалён", "untitled": "Новый чат"});
Object.assign(I18N.en, {"chats": "Chats", "new_chat": "New chat", "no_chats": "No chats yet — ask a question", "cancel": "Cancel", "del_chat_t": "Delete this chat?", "del_chat_d": "The chat “{t}” will be permanently deleted.", "del_doc_t": "Delete the document?", "del_doc_d": "“{t}” and all its fragments will be deleted.", "del_all_docs_t": "Delete all documents?", "del_all_chats_t": "Delete all chats?", "irreversible": "This cannot be undone.", "del_acc_t": "Delete your account?", "clear_hist": "Delete all chats", "clear_hist_d": "Documents are kept", "chat_deleted": "Chat deleted", "untitled": "New chat"});

Object.assign(I18N.kk, {"gate_t": "Жалғастыру үшін кіріңіз", "gate_ask": "Сұрақ қою үшін кіріңіз немесе аккаунт құрыңыз — бұл бір минут алады.", "gate_upload": "Құжат жүктеу үшін кіріңіз немесе аккаунт құрыңыз — бұл бір минут алады.", "gate_any": "Бұл мүмкіндік тек аккаунтпен қолжетімді.", "sign_in": "Кіру", "sign_up": "Аккаунт құру", "later": "Кейінірек", "anon": "Қонақ", "anon_hint": "Кіру немесе тіркелу"});
Object.assign(I18N.ru, {"gate_t": "Войдите, чтобы продолжить", "gate_ask": "Чтобы задать вопрос, войдите или создайте аккаунт — это займёт минуту.", "gate_upload": "Чтобы загрузить документ, войдите или создайте аккаунт — это займёт минуту.", "gate_any": "Эта возможность доступна после входа.", "sign_in": "Войти", "sign_up": "Создать аккаунт", "later": "Позже", "anon": "Гость", "anon_hint": "Войти или зарегистрироваться"});
Object.assign(I18N.en, {"gate_t": "Sign in to continue", "gate_ask": "To ask a question, sign in or create an account — it takes a minute.", "gate_upload": "To upload a document, sign in or create an account — it takes a minute.", "gate_any": "This is available after you sign in.", "sign_in": "Sign in", "sign_up": "Create account", "later": "Later", "anon": "Guest", "anon_hint": "Sign in or sign up"});

Object.assign(I18N.kk, {"gate_profile": "Профиль аккаунтпен қолжетімді.", "gate_data": "Құжаттар мен чаттар кіргеннен кейін сақталады.", "gate_account": "Кіріңіз немесе аккаунт құрыңыз — бір минут алады."});
Object.assign(I18N.ru, {"gate_profile": "Профиль доступен после входа.", "gate_data": "Документы и чаты сохраняются после входа.", "gate_account": "Войдите или создайте аккаунт — это займёт минуту."});
Object.assign(I18N.en, {"gate_profile": "Your profile is available after you sign in.", "gate_data": "Documents and chats are saved once you sign in.", "gate_account": "Sign in or create an account — it takes a minute."});

Object.assign(I18N.kk, {"mm_model": "Модель", "mm_style": "Жауап стилі", "lite": "Mind Lite", "lite_d": "Құжаттар бойынша жылдам әрі нақты жауаптар", "free": "Тегін", "pro": "Mind Pro", "pro_d": "Үлкен құжаттар мен кестелерді терең талдау", "soon": "Жақында", "pro_toast": "Mind Pro әзірленуде — жақында қолжетімді болады", "concise_d": "1–3 сөйлем", "balanced_d": "Негізгі мәліметтері бар жауап", "detailed_d": "Барлық тармақтарымен толық"});
Object.assign(I18N.ru, {"mm_model": "Модель", "mm_style": "Стиль ответа", "lite": "Mind Lite", "lite_d": "Быстрые и точные ответы по документам", "free": "Бесплатно", "pro": "Mind Pro", "pro_d": "Глубокий анализ больших документов и таблиц", "soon": "Скоро", "pro_toast": "Mind Pro в разработке — скоро будет доступна", "concise_d": "1–3 предложения", "balanced_d": "Ответ с ключевыми деталями", "detailed_d": "Подробно, со всеми пунктами"});
Object.assign(I18N.en, {"mm_model": "Model", "mm_style": "Answer style", "lite": "Mind Lite", "lite_d": "Fast, accurate answers from your documents", "free": "Free", "pro": "Mind Pro", "pro_d": "Deep analysis of large documents and tables", "soon": "Soon", "pro_toast": "Mind Pro is in development — coming soon", "concise_d": "1–3 sentences", "balanced_d": "Answer with the key details", "detailed_d": "Thorough, covering every point"});
Object.assign(I18N.kk, {"pro_d": "Беттерді «көреді»: PDF-тағы кестелер, графиктер мен сызбалар", "vision_seen": "Mind Pro беттерді қарады", "tab_cmp": "Салыстыру", "cmp_h": "Нұсқаларды салыстыру", "cmp_sub": "Келісімшарттың, ереженің немесе нұсқаулықтың екі нұсқасын жүктеңіз — не қосылғанын, өшірілгенін және өзгергенін көресіз.", "cmp_old": "Бұрынғы", "cmp_new": "Жаңа", "cmp_go": "Салыстыру", "cmp_need": "Салыстыру үшін құжаттың екі нұсқасын жүктеңіз", "cmp_added": "қосылды", "cmp_removed": "өшірілді", "cmp_changed": "өзгерді", "cmp_similar": "сәйкестік", "cmp_same": "Құжаттардың мәтіні бірдей", "cmp_points": "Негізгі өзгерістер", "cmp_attention": "Назар аударыңыз", "cmp_all": "Барлық өзгерістер", "comparing": "Нұсқаларды салыстырып жатырмын…", "cmp_pick2": "Екі түрлі құжатты таңдаңыз", "cmp_trunc": "Алғашқы 300 өзгеріс көрсетілген"});
Object.assign(I18N.ru, {"pro_d": "«Видит» страницы: таблицы, графики и схемы в PDF", "vision_seen": "Mind Pro посмотрел страницы", "tab_cmp": "Сравнение", "cmp_h": "Сравнение версий", "cmp_sub": "Загрузите две версии договора, регламента или инструкции — и увидите, что добавили, удалили и изменили.", "cmp_old": "Было", "cmp_new": "Стало", "cmp_go": "Сравнить", "cmp_need": "Загрузите две версии документа, чтобы сравнить их", "cmp_added": "добавлено", "cmp_removed": "удалено", "cmp_changed": "изменено", "cmp_similar": "совпадение", "cmp_same": "Тексты документов совпадают", "cmp_points": "Главные изменения", "cmp_attention": "Обратите внимание", "cmp_all": "Все изменения", "comparing": "Сравниваю версии…", "cmp_pick2": "Выберите два разных документа", "cmp_trunc": "Показаны первые 300 изменений"});
Object.assign(I18N.en, {"pro_d": "“Sees” the pages: tables, charts and diagrams in PDFs", "vision_seen": "Mind Pro looked at the pages", "tab_cmp": "Compare", "cmp_h": "Compare versions", "cmp_sub": "Upload two versions of a contract, policy or instruction — and see what was added, removed and changed.", "cmp_old": "Before", "cmp_new": "After", "cmp_go": "Compare", "cmp_need": "Upload two versions of a document to compare them", "cmp_added": "added", "cmp_removed": "removed", "cmp_changed": "changed", "cmp_similar": "match", "cmp_same": "The documents have the same text", "cmp_points": "Key changes", "cmp_attention": "Pay attention", "cmp_all": "All changes", "comparing": "Comparing versions…", "cmp_pick2": "Choose two different documents", "cmp_trunc": "Showing the first 300 changes"});
Object.assign(I18N.kk, {"exporting": "Файл дайындалуда…", "export_as": "Жүктеп алу", "mode_quiz": "Тест", "mode_cards": "Карточкалар", "cards_intro": "Карточкалар саны", "cards_start": "Карточкаларды бастау", "cards_gen": "Карточкалар жасалуда…", "flip": "Жауапты көру үшін басыңыз", "again": "Қайталау", "know": "Білемін", "card_n": "Карточка", "left": "қалды", "cards_done": "Барлық карточка меңгерілді!", "cards_stat": "Бірден білдіңіз: {k} / {n}", "cards_again": "Қайтадан", "new_cards": "Жаңа карточкалар", "quiz_new_note": "Әр жолы — жаңа сұрақтар"});
Object.assign(I18N.ru, {"exporting": "Готовлю файл…", "export_as": "Скачать", "mode_quiz": "Тест", "mode_cards": "Карточки", "cards_intro": "Количество карточек", "cards_start": "Начать карточки", "cards_gen": "Создаю карточки…", "flip": "Нажмите, чтобы увидеть ответ", "again": "Повторить", "know": "Знаю", "card_n": "Карточка", "left": "осталось", "cards_done": "Все карточки выучены!", "cards_stat": "Знали сразу: {k} из {n}", "cards_again": "Пройти снова", "new_cards": "Новые карточки", "quiz_new_note": "Каждый раз — новые вопросы"});
Object.assign(I18N.en, {"exporting": "Preparing the file…", "export_as": "Download", "mode_quiz": "Quiz", "mode_cards": "Flashcards", "cards_intro": "Number of cards", "cards_start": "Start flashcards", "cards_gen": "Creating flashcards…", "flip": "Tap to see the answer", "again": "Again", "know": "I know it", "card_n": "Card", "left": "left", "cards_done": "All cards learned!", "cards_stat": "Known at once: {k} of {n}", "cards_again": "Go again", "new_cards": "New cards", "quiz_new_note": "New questions every time"});
Object.assign(I18N.kk, {"set_plan": "Тариф", "plan_sub": "Тегін нұсқада не бар және Mind Pro-да не бар", "plan_current": "Сіздің тарифіңіз", "plan_free_price": "Тегін", "plan_pro_price": "Жазылым бойынша", "plan_soon": "Жақында", "plan_plus": "Lite-тағы барлығы, сонымен қатар:", "pro_toast": "Mind Pro — жазылым бойынша, жақында қолжетімді болады",
  "lite_f": ["Құжаттар бойынша жауаптар — бетке сілтемемен", "PDF, DOCX, PPTX, XLSX, фото және сканерлер (OCR)", "Қазақ, орыс және ағылшын тілдері", "Сөздер бойынша ғана емес, мағына бойынша іздеу", "Құжат картасы, тест және карточкалар", "Құжат нұсқаларын салыстыру", "Жауаптарды PDF және Word-қа жүктеу"],
  "pro_f": ["«Көру»: PDF беттеріндегі кестелерді, графиктер мен сызбаларды оқиды", "Екі есе көп контекст — үлкен құжаттарды терең талдау", "Қай беттерді қарағанын көрсетеді", "Жаңа мүмкіндіктерге ерте қолжетімділік"]});
Object.assign(I18N.ru, {"set_plan": "Тариф", "plan_sub": "Что входит в бесплатную версию и что — в Mind Pro", "plan_current": "Ваш тариф", "plan_free_price": "Бесплатно", "plan_pro_price": "По подписке", "plan_soon": "Скоро", "plan_plus": "Всё из Lite, а также:", "pro_toast": "Mind Pro — по подписке, скоро будет доступна",
  "lite_f": ["Ответы по документам — со ссылкой на страницу", "PDF, DOCX, PPTX, XLSX, фото и сканы (OCR)", "Казахский, русский и английский", "Поиск по смыслу, а не только по словам", "Карта документа, тест и карточки", "Сравнение версий документа", "Экспорт ответов в PDF и Word"],
  "pro_f": ["«Зрение»: читает таблицы, графики и схемы прямо со страниц PDF", "Вдвое больше контекста — глубокий анализ больших документов", "Показывает, какие страницы просмотрел", "Ранний доступ к новым функциям"]});
Object.assign(I18N.en, {"set_plan": "Plan", "plan_sub": "What the free version includes and what Mind Pro adds", "plan_current": "Your plan", "plan_free_price": "Free", "plan_pro_price": "Subscription", "plan_soon": "Coming soon", "plan_plus": "Everything in Lite, plus:", "pro_toast": "Mind Pro is a subscription — coming soon",
  "lite_f": ["Answers from your documents — with page references", "PDF, DOCX, PPTX, XLSX, photos and scans (OCR)", "Kazakh, Russian and English", "Search by meaning, not just by words", "Document map, quiz and flashcards", "Compare document versions", "Export answers to PDF and Word"],
  "pro_f": ["“Vision”: reads tables, charts and diagrams right from PDF pages", "Twice the context — deep analysis of large documents", "Shows which pages it looked at", "Early access to new features"]});
Object.assign(I18N.kk, {"th_read": "Сұрақты оқып жатырмын", "th_search": "Құжаттардан іздеп жатырмын — сөздер мен мағына бойынша", "th_found": "{n} үзінді таптым · {where}", "th_none": "Дәл сәйкестік жоқ — бүкіл құжатты қараймын", "th_vision": "Беттерді қарап жатырмын: {pages}", "th_write": "Жауапты құрастырып жатырмын", "th_h1": "Деректерді дереккөздермен салыстырып жатырмын", "th_h2": "Сандар мен күндерді тексеріп жатырмын", "th_h3": "Жауаптың құрылымын жасап жатырмын", "th_done": "{s} с ойландым", "too_many_req": "Сұраулар тым көп — сәл күте тұрыңыз",
  "ld_read": "Құжатты толық оқып жатырмын", "ld_dates": "Мерзімдер мен күндерді табамын", "ld_numbers": "Негізгі сандарды жазып аламын", "ld_reqs": "Талаптарды жинаймын", "ld_terms": "Глоссарий құрастырамын", "ld_facts": "Маңызды деректерді таңдаймын", "ld_questions": "Сұрақтар ойлап табамын", "ld_options": "Сенімді жауап нұсқаларын іріктеймін", "ld_check": "Жауаптарды мәтін бойынша тексеремін", "ld_cards": "Карточкаларды жазамын", "ld_memo": "Есте сақтауға тұрарлықты таңдаймын", "ld_parse": "Екі нұсқаны да талдап жатырмын", "ld_match": "Тармақтарды салыстырамын", "ld_words": "Өзгерістерді сөз бойынша іздеймін", "ld_weigh": "Ненің маңызды екенін бағалаймын"});
Object.assign(I18N.ru, {"th_read": "Читаю вопрос", "th_search": "Ищу в документах — по словам и по смыслу", "th_found": "Нашёл {n} фрагм. · {where}", "th_none": "Точных совпадений нет — смотрю документ целиком", "th_vision": "Смотрю страницы: {pages}", "th_write": "Формулирую ответ", "th_h1": "Сверяю факты с источниками", "th_h2": "Проверяю цифры и даты", "th_h3": "Выстраиваю структуру ответа", "th_done": "Думал {s} с", "too_many_req": "Слишком много запросов — подождите немного",
  "ld_read": "Читаю документ целиком", "ld_dates": "Нахожу сроки и даты", "ld_numbers": "Выписываю ключевые цифры", "ld_reqs": "Собираю требования", "ld_terms": "Составляю глоссарий", "ld_facts": "Выбираю важные факты", "ld_questions": "Придумываю вопросы", "ld_options": "Подбираю правдоподобные варианты", "ld_check": "Проверяю ответы по тексту", "ld_cards": "Пишу карточки", "ld_memo": "Выбираю, что стоит запомнить", "ld_parse": "Разбираю обе версии", "ld_match": "Сопоставляю пункты", "ld_words": "Ищу изменения по словам", "ld_weigh": "Оцениваю, что важно"});
Object.assign(I18N.en, {"th_read": "Reading the question", "th_search": "Searching the documents — by words and by meaning", "th_found": "Found {n} passages · {where}", "th_none": "No exact matches — reading the whole document", "th_vision": "Looking at the pages: {pages}", "th_write": "Writing the answer", "th_h1": "Checking facts against the sources", "th_h2": "Verifying numbers and dates", "th_h3": "Structuring the answer", "th_done": "Thought for {s}s", "too_many_req": "Too many requests — please wait a moment",
  "ld_read": "Reading the whole document", "ld_dates": "Finding deadlines and dates", "ld_numbers": "Collecting key numbers", "ld_reqs": "Gathering requirements", "ld_terms": "Building a glossary", "ld_facts": "Picking the important facts", "ld_questions": "Writing questions", "ld_options": "Choosing plausible options", "ld_check": "Checking answers against the text", "ld_cards": "Writing flashcards", "ld_memo": "Choosing what is worth remembering", "ld_parse": "Parsing both versions", "ld_match": "Matching clauses", "ld_words": "Finding word-level changes", "ld_weigh": "Weighing what matters"});
Object.assign(I18N.kk, {"fix_mistakes": "Қателерді түзету", "cards_hard": "Қиындарын қайталау"});
Object.assign(I18N.ru, {"fix_mistakes": "Исправить ошибки", "cards_hard": "Повторить трудные"});
Object.assign(I18N.en, {"fix_mistakes": "Fix mistakes", "cards_hard": "Review the hard ones"});

const $ = (s) => document.querySelector(s);
const state = {
  lang: pickLang(),
  docs: [],
  selected: new Set(),
  status: null,
  busy: false,
  view: "chat",
  mapDoc: null,
  mapCache: {},
  cmpA: null, cmpB: null, cmp: null,
  quizMode: "quiz", cards: null, cardsN: 10,  // режим вкладки «Проверка знаний»: тест или карточки  // сравнение версий: выбранные документы и последний результат
  quizDoc: null,
  quiz: null,
  quizN: 5,
  user: null,
  log: [],
  setTab: "profile",
  chatId: null,
  chats: [],
};

function pickLang() {
  try {
    const saved = localStorage.getItem("mind_lang");
    if (saved && I18N[saved]) return saved;
  } catch (_) {}
  const nav = (navigator.language || "kk").slice(0, 2);
  return nav === "ru" ? "ru" : nav === "en" ? "en" : "kk";
}


const L = (key) => I18N[state.lang][key] ?? I18N.ru[key] ?? key;

function applyI18n() {
  document.documentElement.lang = state.lang;
  document.querySelectorAll("[data-i18n]").forEach((el) => (el.textContent = L(el.dataset.i18n)));
  document.querySelectorAll("[data-i18n-html]").forEach((el) => (el.innerHTML = L(el.dataset.i18nHtml)));
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => (el.placeholder = L(el.dataset.i18nPlaceholder)));
  document.querySelectorAll("[data-i18n-title]").forEach((el) => (el.title = L(el.dataset.i18nTitle)));
  renderDocs();
  renderScope();
  renderUser();
  if ($("#modelLabel")) renderModelPicker();
  if (state.view === "map") renderMap();
  if (state.view === "quiz") renderQuiz();
  if (state.view === "compare") renderCompare();
  if (!$("#settings").hidden) renderSettings();
  if (state.log.length && !state.busy) renderLog([...state.log]);
}

/* ================= API ================= */
async function api(path, options = {}) {
  const res = await fetch(path, options);
  if (res.status === 401) { requireLogin("any"); throw new Error("401"); }
  if (res.status === 429) throw new Error(L("too_many_req"));
  if (!res.ok) {
    const text = await res.text();
    let detail = text;
    try { detail = JSON.parse(text).detail || text; } catch (_) {}
    throw new Error(typeof detail === "string" ? detail : res.statusText);
  }
  return res.json();
}

function toast(text, isError = false) {
  const el = $("#toast");
  el.textContent = text;
  el.classList.toggle("error", isError);
  el.classList.add("show");
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => el.classList.remove("show"), 3200);
}

/* ================= markdown ================= */
const icon = (name) => `<svg><use href="#i-${name}"/></svg>`;

// «стр. 2» / «бет 2» / «p. 2» — на текущем языке интерфейса (сервер присылает подпись на языке ответа)
const LOC_NAMES = {
  page: { kk: "бет", ru: "стр.", en: "p." }, slide: { kk: "слайд", ru: "слайд", en: "slide" },
  sheet: { kk: "парақ", ru: "лист", en: "sheet" }, section: { kk: "бөлім", ru: "раздел", en: "section" },
  image: { kk: "сурет", ru: "изображение", en: "image" },
};
function locLabel(item) {
  const loc = item && item.loc;
  if (!loc) return (item && item.loc_label) || "";
  const names = LOC_NAMES[loc.type] || LOC_NAMES.section;
  if (loc.type === "image") return names[state.lang];
  return loc.value === null || loc.value === undefined || loc.value === "" ? "" : `${names[state.lang]} ${loc.value}`;
}
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

function inline(s) {
  return esc(s)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*(.+?)\*\*/g, "<b>$1</b>")
    .replace(/(^|[^\w*])\*(?!\s)(.+?)\*(?!\w)/g, "$1<i>$2</i>")
    .replace(/(^|[^\w])_(?!\s)(.+?)_(?!\w)/g, "$1<i>$2</i>")
    .replace(/\[(\d+(?:\s*[,;]\s*\d+)*)\]/g, (_, nums) =>
      nums.split(/[,;]/).map((n) => `<button class="cite" data-n="${n.trim()}">${n.trim()}</button>`).join(""));
}

function md(src) {
  const code = [];
  src = src.replace(/```[\w-]*\n?([\s\S]*?)(```|$)/g, (_, c) => { code.push(c); return `\u0000${code.length - 1}\u0000`; });
  const out = [];
  let list = null, para = [], table = [];
  const flushPara = () => { if (para.length) { out.push(`<p>${para.map(inline).join("<br>")}</p>`); para = []; } };
  const flushList = () => { if (list) { out.push(`<${list.type}>${list.items.map((i) => `<li>${inline(i)}</li>`).join("")}</${list.type}>`); list = null; } };
  const flushTable = () => {
    if (!table.length) return;
    const rows = table.filter((r) => !/^\|?[\s:|-]+\|?$/.test(r)).map((r) => r.replace(/^\||\|$/g, "").split("|").map((c) => c.trim()));
    const [head, ...body] = rows;
    out.push(`<table><thead><tr>${head.map((c) => `<th>${inline(c)}</th>`).join("")}</tr></thead><tbody>${body.map((r) => `<tr>${r.map((c) => `<td>${inline(c)}</td>`).join("")}</tr>`).join("")}</tbody></table>`);
    table = [];
  };
  const flushAll = () => { flushPara(); flushList(); flushTable(); };

  for (const raw of src.split("\n")) {
    const line = raw.trimEnd();
    const codeRef = line.match(/^\u0000(\d+)\u0000$/);
    if (codeRef) { flushAll(); out.push(`<pre><code>${esc(code[+codeRef[1]])}</code></pre>`); continue; }
    if (/^\s*\|.*\|\s*$/.test(line)) { flushPara(); flushList(); table.push(line.trim()); continue; }
    flushTable();
    let m;
    if (!line.trim()) { flushPara(); flushList(); continue; }
    if ((m = line.match(/^#{1,6}\s+(.*)$/))) { flushAll(); out.push(`<h4>${inline(m[1])}</h4>`); continue; }
    if ((m = line.match(/^\s*[-*•]\s+(.*)$/))) { flushPara(); if (!list || list.type !== "ul") { flushList(); list = { type: "ul", items: [] }; } list.items.push(m[1]); continue; }
    if ((m = line.match(/^\s*\d+[.)]\s+(.*)$/))) { flushPara(); if (!list || list.type !== "ol") { flushList(); list = { type: "ol", items: [] }; } list.items.push(m[1]); continue; }
    if (list && /^\s{2,}\S/.test(line)) { list.items[list.items.length - 1] += " " + line.trim(); continue; }
    flushList();
    para.push(line);
  }
  flushAll();
  return out.join("").replace(/\u0000(\d+)\u0000/g, (_, i) => `<code>${esc(code[+i])}</code>`);
}

/* ================= documents ================= */
const IMG_EXT = [".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff", ".gif"];

function extClass(ext) {
  return IMG_EXT.includes(ext) ? "img" : ext.replace(".", "");
}

function fileUrl(docId, loc) {
  let url = `/api/documents/${docId}/file`;
  if (loc && loc.type === "page") url += `#page=${loc.value}`;
  return url;
}

function renderDocs(pending = []) {
  const list = $("#docList");
  list.innerHTML = "";
  for (const d of state.docs) {
    const el = document.createElement("div");
    el.className = "doc" + (state.selected.has(d.id) ? " selected" : "");
    el.innerHTML = `
      <div class="doc-top">
        <div class="doc-ext ${extClass(d.ext)}">${esc(d.ext.replace(".", "").slice(0, 4))}</div>
        <div class="doc-info" title="${esc(d.name)}">
          <div class="doc-name">${esc(d.name)}</div>
          <div class="doc-meta"><span>${d.pages} ${L("pages")}</span><span>${d.chunks} ${L("chunks")}</span>
            ${d.ocr_pages ? `<span class="badge">${L("ocr")} · ${d.ocr_pages}</span>` : ""}
            <span>${(d.lang || "").toUpperCase()}</span></div>
        </div>
      </div>
      <div class="doc-actions">
        <button data-act="summary">${icon("spark")}${L("summary")}</button>
        <button data-act="map">${icon("map")}${L("map_btn")}</button>
        <button data-act="open" title="${L("open")}">${icon("open")}</button>
        <button data-act="delete" class="del" title="${L("delete")}">${icon("trash")}</button>
      </div>`;
    el.querySelector(".doc-info").onclick = () => toggleSelect(d.id);
    el.querySelector('[data-act="summary"]').onclick = () => showSummary(d);
    el.querySelector('[data-act="map"]').onclick = () => { state.mapDoc = d.id; setView("map"); };
    el.querySelector('[data-act="open"]').onclick = () => window.open(fileUrl(d.id), "_blank");
    el.querySelector('[data-act="delete"]').onclick = () => deleteDoc(d);
    list.appendChild(el);
  }
  for (const name of pending) {
    const el = document.createElement("div");
    el.className = "doc pending";
    el.innerHTML = `<div class="doc-top"><div class="doc-ext"><span class="spinner"></span></div><div class="doc-info"><div class="doc-name">${esc(name)}</div><div class="doc-meta">${L("uploading")}</div></div></div>`;
    list.appendChild(el);
  }
  $("#docCount").textContent = state.docs.length;
  $("#docEmpty").style.display = state.docs.length || pending.length ? "none" : "block";
}

function renderScope() {
  const sel = state.docs.filter((d) => state.selected.has(d.id));
  $("#scope").innerHTML = sel.length
    ? `${L("scope_sel")} <b>${sel.map((d) => esc(d.name)).join(", ")}</b>`
    : `${L("scope_all")} · ${state.docs.length}`;
}

function toggleSelect(id) {
  state.selected.has(id) ? state.selected.delete(id) : state.selected.add(id);
  renderDocs();
  renderScope();
}

async function loadDocs() {
  state.docs = await api("/api/documents");
  for (const id of [...state.selected]) if (!state.docs.find((d) => d.id === id)) state.selected.delete(id);
  renderDocs();
  renderScope();
  if (state.view === "map") renderMap();
  if (state.view === "quiz") renderQuiz();
  if (state.view === "compare") renderCompare();
}

async function uploadFiles(files) {
  if (!files.length) return;
  if (state.anon) return requireLogin("upload");
  const names = [...files].map((f) => f.name);
  const dz = $("#dropzone");
  dz.classList.add("busy");
  renderDocs(names);
  const form = new FormData();
  for (const f of files) form.append("files", f);
  try {
    const results = await api("/api/documents", { method: "POST", body: form });
    await loadDocs();
    for (const r of results) {
      if (r.error) toast(`${L("upload_error")}: ${r.name} — ${r.error}`, true);
      else {
        toast(`✅ ${r.name} ${L("uploaded")}`);
        showSummary(r, true);
      }
    }
  } catch (e) {
    toast(`${L("upload_error")}: ${e.message}`, true);
    renderDocs();
  } finally {
    dz.classList.remove("busy");
    $("#fileInput").value = "";
  }
}

async function deleteDoc(d) {
  if (!(await confirmDialog(L("del_doc_t"), L("del_doc_d").replace("{t}", d.name)))) return;
  await api(`/api/documents/${d.id}`, { method: "DELETE" });
  state.selected.delete(d.id);
  await loadDocs();
}

async function showSummary(doc, justUploaded = false) {
  hideWelcome();
  const { body } = addBotMessage();
  const bubble = body.querySelector(".bubble");
  bubble.innerHTML = `<div class="typing"><span></span><span></span><span></span></div>`;
  try {
    const s = await api(`/api/documents/${doc.id}/summary?lang=${state.lang}`);
    const meta = `${doc.pages} ${L("pages")} · ${doc.chunks} ${L("chunks")}${doc.ocr_pages ? ` · ${L("ocr")}: ${doc.ocr_pages}` : ""}`;
    bubble.innerHTML = `<p><b>${justUploaded ? L("doc_ready") : L("summary_title")}: ${esc(doc.name)}</b><br><small style="color:var(--muted)">${meta}</small></p>${md(s.summary || "")}`;
    if (s.questions && s.questions.length) {
      const wrap = document.createElement("div");
      wrap.innerHTML = `<p style="margin-top:10px"><b>${L("ask_these")}</b></p><div class="summary-q"></div>`;
      const qs = wrap.querySelector(".summary-q");
      for (const q of s.questions) qs.appendChild(chip(q));
      if (prefs().suggestions) {
        bubble.appendChild(wrap);
        setSuggestions(s.questions.slice(0, 3));
      }
    }
  } catch (e) {
    bubble.textContent = `${L("error")}: ${e.message}`;
  }
  scrollDown();
}

/* ================= chat ================= */
function hideWelcome() { $("#welcome").style.display = "none"; }

function scrollDown() {
  const chat = $("#chat");
  chat.scrollTop = chat.scrollHeight;
}

function chip(text) {
  const b = document.createElement("button");
  b.type = "button";
  b.className = "chip";
  b.textContent = text;
  b.onclick = () => ask(text);
  return b;
}

function setSuggestions(questions) {
  const box = $("#suggestions");
  box.innerHTML = "";
  for (const q of questions) box.appendChild(chip(q));
}

function addUserMessage(text) {
  const el = document.createElement("div");
  el.className = "msg user";
  el.innerHTML = `<div class="bubble"></div>`;
  el.querySelector(".bubble").textContent = text;
  $("#messages").appendChild(el);
  scrollDown();
}

const BOT_AVATAR = `<div class="avatar"><img src="/static/favicon.svg" alt=""></div>`;

function addBotMessage() {
  const el = document.createElement("div");
  el.className = "msg bot";
  el.innerHTML = `${BOT_AVATAR}<div class="body"><div class="bubble"></div></div>`;
  $("#messages").appendChild(el);
  return { el, body: el.querySelector(".body") };
}

function renderSources(body, sources, cited, evidenceQuery) {
  const byN = Object.fromEntries(sources.map((s) => [s.n, s]));
  const shown = cited.map((n) => byN[n]).filter(Boolean);
  const p = prefs();
  if (p.show_trust) {
  const trust = document.createElement("div");
  trust.className = "trust " + (shown.length ? "ok" : "warn");
  trust.textContent = shown.length ? "✔ " + L("trust_ok").replace("{n}", shown.length) : "⚠ " + L("trust_none");
  body.appendChild(trust);
  }
  if (!shown.length || !p.show_sources) return;
  const chips = document.createElement("div");
  chips.className = "sources";
  const open = (n) => {
    const s = byN[n];
    if (!s) return;
    chips.querySelectorAll(".src-chip").forEach((c) => c.classList.toggle("active", +c.dataset.n === +n));
    openEvidence(s.chunk_id, evidenceQuery);
  };
  for (const s of shown) {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "src-chip";
    b.dataset.n = s.n;
    b.innerHTML = `<span class="n">${s.n}</span><span class="t">${esc(s.doc_name)}${locLabel(s) ? " · " + esc(locLabel(s)) : ""}</span>`;
    b.onclick = () => open(s.n);
    chips.appendChild(b);
  }
  body.appendChild(chips);
  body.querySelectorAll(".bubble .cite").forEach((c) => (c.onclick = () => open(c.dataset.n)));
}

/* ================= панель доказательства ================= */
const VOWELS = new Set("аеиоуыэюяьйіәөұүaeiouy");

function stems(text) {
  return (text.toLowerCase().replace(/ё/g, "е").match(/[\p{L}\p{N}]+/gu) || [])
    .filter((w) => w.length >= 2)
    .map((w) => {
      w = w.slice(0, 6);
      if (w.length >= 5 && VOWELS.has(w[w.length - 1])) w = w.slice(0, -1);
      return w;
    });
}

// Подсвечивает предложения фрагмента, на которых основан ответ (та же логика, что на сервере)
function highlightText(text, query) {
  const q = new Set(stems(query));
  const parts = text.replace(/(^|\n)#{1,6} /g, "$1").replace(/\n/g, " ").split(/(?<=[.!?…;])\s+/);
  const scores = parts.map((p) => stems(p).filter((t) => q.has(t)).length);
  const best = Math.max(0, ...scores);
  return parts.map((p, i) => (best > 0 && scores[i] >= Math.max(1, best * 0.5) ? `<mark>${esc(p)}</mark>` : esc(p))).join(" ");
}

async function openEvidence(chunkId, query) {
  if (!chunkId) return;
  query = (query || "").slice(0, 400);
  $("#evidence").classList.add("open");
  $("#scrim").classList.add("show");
  $("#evName").textContent = "…";
  $("#evPage").innerHTML = `<span class="spinner"></span>`;
  $("#evQuote").innerHTML = "";
  try {
    const info = await api(`/api/chunk?chunk=${encodeURIComponent(chunkId)}&lang=${state.lang}`);
    $("#evName").textContent = `${info.doc_name}${locLabel(info) ? " · " + locLabel(info) : ""}`;
    $("#evOpen").href = fileUrl(info.doc_id, info.loc);
    $("#evQuote").innerHTML = highlightText(info.text, query);
    if (!info.has_page) { $("#evPage").innerHTML = ""; return; }
    const img = new Image();
    img.alt = info.loc_label;
    img.onload = () => { $("#evPage").innerHTML = ""; $("#evPage").appendChild(img); };
    img.onerror = () => { $("#evPage").innerHTML = ""; };
    img.src = `/api/evidence.png?chunk=${encodeURIComponent(chunkId)}&q=${encodeURIComponent(query)}`;
  } catch (e) {
    $("#evPage").innerHTML = "";
    $("#evQuote").textContent = `${L("error")}: ${e.message}`;
  }
}

function closeEvidence() {
  $("#evidence").classList.remove("open");
  $("#scrim").classList.remove("show");
}

function addTools(body, msg, question) {
  const tools = document.createElement("div");
  tools.className = "msg-tools";
  const button = (label, onclick) => {
    const b = document.createElement("button");
    b.type = "button";
    b.textContent = label;
    b.onclick = onclick;
    tools.appendChild(b);
  };
  button(L("copy"), async () => {
    try { await navigator.clipboard.writeText(msg.text); toast(L("copied")); } catch (_) {}
  });
  const exp = (format) => () => downloadExport({ format, kind: "answer", question: question || "", answer: msg.text, sources: msg.sources || [] });
  button("PDF", exp("pdf"));
  button("Word", exp("docx"));
  body.appendChild(tools);
}

// «Ход мыслей», как у Claude: реальные шаги (поиск, найденные страницы, ответ) + время.
// Пока модель думает — шаги видны и текущий переливается; с первым словом ответа блок сворачивается в «Думал N с».
function createThinking(body) {
  const el = document.createElement("div");
  el.className = "think live";
  el.innerHTML = `<button type="button" class="think-head"><span class="think-title"></span><span class="think-time"></span>${icon("chev")}</button><ol class="think-steps"></ol>`;
  body.insertBefore(el, body.querySelector(".bubble"));
  const title = el.querySelector(".think-title"), list = el.querySelector(".think-steps"), time = el.querySelector(".think-time");
  const t0 = Date.now();
  const secs = () => Math.max(1, Math.round((Date.now() - t0) / 1000));
  const clock = setInterval(() => { time.textContent = `${secs()} ${state.lang === "en" ? "s" : "с"}`; }, 500);
  let hintTimer = 0, done = false;
  el.querySelector(".think-head").onclick = () => { if (done) el.classList.toggle("open"); };
  const step = (text) => {
    if (done) return;
    list.querySelectorAll("li").forEach((li) => li.classList.add("ok"));
    const li = document.createElement("li");
    li.textContent = text;
    list.appendChild(li);
    title.textContent = text;
    scrollDown();
  };
  return {
    step,
    hints() {  // пока ждём первое слово модели — показываем, над чем она работает
      let i = 0;
      clearInterval(hintTimer);
      hintTimer = setInterval(() => { if (i < 3) step(L(`th_h${++i}`)); else clearInterval(hintTimer); }, 2600);
    },
    finish() {
      if (done) return;
      done = true;
      clearInterval(clock);
      clearInterval(hintTimer);
      list.querySelectorAll("li").forEach((li) => li.classList.add("ok"));
      el.classList.remove("live");
      title.textContent = L("th_done").replace("{s}", secs());
      time.textContent = "";
    },
  };
}

// Mind Pro: какие страницы модель «посмотрела» глазами (кнопки открывают PDF на этой странице)
function addVisionNote(body, pages) {
  const note = document.createElement("div");
  note.className = "vision-note";
  note.innerHTML = `${icon("eye")}<span>${L("vision_seen")}:</span>` + pages.map((p) =>
    `<a href="${fileUrl(p.doc_id, p.loc)}" target="_blank" rel="noopener">${esc(locLabel(p) || p.doc_name)}</a>`).join("");
  body.insertBefore(note, body.querySelector(".bubble"));
}

async function ask(question) {
  question = question.trim();
  if (!question || state.busy) return;
  if (state.anon) return requireLogin("ask", question);
  state.busy = true;
  $("#sendBtn").disabled = true;
  hideWelcome();
  $("#suggestions").innerHTML = "";
  document.querySelectorAll("#messages .followups").forEach((el) => el.remove());
  addUserMessage(question);
  state.log.push({ role: "user", text: question });
  const { body } = addBotMessage();
  const bubble = body.querySelector(".bubble");
  bubble.hidden = true;  // до первого слова ответа виден «ход мыслей»
  const think = createThinking(body);
  think.step(L("th_read"));
  scrollDown();

  let text = "", sources = [], cited = [], frame = 0, finished = false, entry = null, vision = null;
  const paint = () => { frame = 0; bubble.hidden = false; bubble.innerHTML = md(text); scrollDown(); };
  // ответ готов на событии «done» — подсказки следующего вопроса приходят чуть позже, не держим ввод
  const finish = () => {
    if (finished) return;
    finished = true;
    think.finish();
    if (frame) cancelAnimationFrame(frame);
    paint();
    renderSources(body, sources, cited, question + " " + text.slice(0, 300));
    const byN = Object.fromEntries(sources.map((x) => [x.n, x]));
    entry = { role: "bot", text, sources: cited.map((n) => byN[n]).filter(Boolean), vision };
    state.log.push(entry);
    addTools(body, entry, question);
    state.busy = false;
    $("#sendBtn").disabled = false;
    scrollDown();
  };

  try {
    const res = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, doc_ids: state.selected.size ? [...state.selected] : null, chat_id: state.chatId }),
    });
    if (res.status === 401) { requireLogin("ask", question); return; }
    if (res.status === 429) throw new Error(L("too_many_req"));
    if (!res.ok || !res.body) throw new Error(await res.text());
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buf = "";
    for (;;) {
      const { value, done } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });
      let idx;
      while ((idx = buf.indexOf("\n\n")) >= 0) {
        const line = buf.slice(0, idx).trim();
        buf = buf.slice(idx + 2);
        if (!line.startsWith("data:")) continue;
        const ev = JSON.parse(line.slice(5));
        if (ev.type === "chat") { state.chatId = ev.id; }
        else if (ev.type === "status") {
          think.step(L(ev.step === "search" ? "th_search" : "th_write"));
          if (ev.step === "write") think.hints();
        }
        else if (ev.type === "sources") { sources = ev.sources; think.step(foundStep(sources)); }
        else if (ev.type === "vision") {
          vision = ev.pages;
          addVisionNote(body, ev.pages);
          think.step(L("th_vision").replace("{pages}", ev.pages.map(locLabel).join(", ")));
        }
        else if (ev.type === "delta") { if (!text) think.finish(); text += ev.text; if (!frame) frame = requestAnimationFrame(paint); }
        else if (ev.type === "done") { cited = ev.cited || []; finish(); }
        else if (ev.type === "followups") { if (entry) entry.followups = ev.items; addFollowups(body, ev.items); }
        else if (ev.type === "error") toast(`${L("error")}: ${ev.message}`, true);
      }
    }
    finish();
    loadChats();  // после конца потока — сервер к этому моменту сохранил ответ в чат
  } catch (e) {
    think.finish();
    if (!finished) { bubble.hidden = false; bubble.textContent = `${L("error")}: ${e.message}`; }
  } finally {
    if (!finished) {
      state.busy = false;
      $("#sendBtn").disabled = false;
    }
    scrollDown();
  }
}

// «Нашёл 6 фрагм. · Ереже.pdf · стр. 2, 3» — какие места документов бот читает
function foundStep(sources) {
  if (!sources.length) return L("th_none");
  const byDoc = {};
  for (const x of sources) (byDoc[x.doc_name] ??= []).push(locLabel(x));
  const where = Object.entries(byDoc).slice(0, 2).map(([doc, locs]) => {
    const uniq = [...new Set(locs.filter(Boolean))];
    return uniq.length ? `${doc} · ${uniq.slice(0, 3).join(", ")}` : doc;
  }).join("; ");
  return L("th_found").replace("{n}", sources.length).replace("{where}", where);
}

// Подсказки следующего вопроса — только под последним ответом
function addFollowups(body, items) {
  if (!items || !items.length || body !== $("#messages").lastElementChild?.querySelector(".body")) return;
  document.querySelectorAll("#messages .followups").forEach((el) => el.remove());
  const box = document.createElement("div");
  box.className = "followups";
  for (const q of items) {
    const b = document.createElement("button");
    b.type = "button";
    b.innerHTML = `${icon("chev")}<span>${esc(q)}</span>`;
    b.onclick = () => ask(q);
    box.appendChild(b);
  }
  body.appendChild(box);
  scrollDown();
}

/* ---------- экспорт в PDF / DOCX ---------- */
async function downloadExport(payload) {
  if (state.anon) return requireLogin("any");
  toast(L("exporting"));
  try {
    const res = await fetch("/api/export", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ lang: state.lang, ...payload }),
    });
    if (res.status === 401) return requireLogin("any");
    if (!res.ok) throw new Error((await res.json().catch(() => ({}))).detail || res.status);
    const cd = res.headers.get("Content-Disposition") || "";
    const name = decodeURIComponent((cd.match(/filename\*=UTF-8''([^;]+)/) || [])[1] || `mind-ai.${payload.format}`);
    const url = URL.createObjectURL(await res.blob());
    const a = Object.assign(document.createElement("a"), { href: url, download: name });
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 2000);
  } catch (e) {
    toast(`${L("error")}: ${e.message}`, true);
  }
}

/* ================= режимы ================= */
function setView(view) {
  state.view = view;
  $("#viewChat").hidden = view !== "chat";
  $("#viewMap").hidden = view !== "map";
  $("#viewQuiz").hidden = view !== "quiz";
  $("#viewCompare").hidden = view !== "compare";
  document.querySelectorAll("#tabs button").forEach((b) => b.classList.toggle("active", b.dataset.view === view));
  $("#sidebar").classList.remove("open");
  if (view === "map") renderMap();
  if (view === "quiz") renderQuiz();
  if (view === "compare") renderCompare();
}

function currentDoc(key) {
  let doc = state.docs.find((d) => d.id === state[key]);
  if (!doc && state.docs.length) {
    doc = state.docs[state.docs.length - 1];
    state[key] = doc.id;
  }
  return doc;
}

function renderPicker(selector, key, onChange) {
  const box = $(selector);
  box.innerHTML = "";
  if (state.docs.length < 2) return;
  const active = currentDoc(key);
  for (const d of state.docs) {
    const b = document.createElement("button");
    b.type = "button";
    b.className = d.id === active.id ? "active" : "";
    b.innerHTML = `<span class="mini-ext">${esc(d.ext.replace(".", "").slice(0, 4))}</span><span>${esc(d.name)}</span>`;
    b.onclick = () => { state[key] = d.id; onChange(); };
    box.appendChild(b);
  }
}

// пустое состояние — это и есть кнопка загрузки (клик или перетаскивание файла)
const emptyState = () => `<button type="button" class="empty-state" data-upload><div class="big">${icon("upload")}</div><b>${L("need_doc_t")}</b>${L("need_doc")}</button>`;
const loadingState = (text) => `<div class="loading"><span class="spinner"></span>${text}</div>`;
// Долгая генерация (15–30 с): этапы сменяют друг друга, полоса медленно растёт — видно, что работа идёт
const STAGES = {
  map: ["ld_read", "ld_dates", "ld_numbers", "ld_reqs", "ld_terms"],
  quiz: ["ld_read", "ld_facts", "ld_questions", "ld_options", "ld_check"],
  cards: ["ld_read", "ld_memo", "ld_cards", "ld_check"],
  compare: ["ld_parse", "ld_match", "ld_words", "ld_weigh"],
};
const stagedState = (kind) => `<div class="loading staged" data-kind="${kind}" data-start="${Date.now()}">
  <span class="spinner"></span><div class="staged-body"><div class="staged-t">${L(STAGES[kind][0])}</div><div class="staged-bar"><i></i></div></div></div>`;
setInterval(() => {
  document.querySelectorAll(".staged").forEach((el) => {
    const t = (Date.now() - +el.dataset.start) / 1000;
    const keys = STAGES[el.dataset.kind];
    const text = L(keys[Math.min(keys.length - 1, Math.floor(t / 3.2))]);
    const label = el.querySelector(".staged-t");
    if (label.textContent !== text) { label.textContent = text; label.classList.remove("in"); void label.offsetWidth; label.classList.add("in"); }
    el.querySelector(".staged-bar i").style.width = `${Math.round(92 * (1 - Math.exp(-t / 14)))}%`;
  });
}, 300);
const locLink = (item) => (item.chunk_id
  ? ` <button class="loc-link" data-chunk="${esc(item.chunk_id)}" data-q="${esc(item.quote || "")}">${esc(locLabel(item) || L("evidence"))}</button>`
  : "");

/* ---------- карта документа ---------- */
async function renderMap() {
  renderPicker("#mapPicker", "mapDoc", renderMap);
  const body = $("#mapBody");
  const doc = currentDoc("mapDoc");
  if (!doc) { body.innerHTML = emptyState(); return; }
  const key = `${doc.id}:${state.lang}`;
  if (!state.mapCache[key]) {
    body.innerHTML = stagedState("map");
    try {
      state.mapCache[key] = await api(`/api/documents/${doc.id}/insights?lang=${state.lang}`);
    } catch (e) {
      body.innerHTML = `<div class="empty-state">${L("error")}: ${esc(e.message)}</div>`;
      return;
    }
    if (state.view !== "map" || state.mapDoc !== doc.id) return;  // пользователь уже переключился
  }
  paintMap(doc, state.mapCache[key]);
}

function checklistKey(doc) { return `docmind_check_${doc.id}_${state.lang}`; }

function paintMap(doc, m) {
  let done = [];
  try { done = JSON.parse(localStorage.getItem(checklistKey(doc)) || "[]"); } catch (_) {}
  const none = `<div class="none">${L("nothing")}</div>`;
  const reqDone = m.requirements.filter((_, i) => done.includes(i)).length;
  $("#mapBody").innerHTML = `
    <div class="map-hero">
      <h3>${esc(m.title || doc.name)}</h3>
      <p>${esc(m.summary || "")}</p>
      <div class="map-stats">
        <div><b>${doc.pages}</b>${L("stat_pages")}</div>
        <div><b>${m.timeline.length}</b>${L("stat_dates")}</div>
        <div><b>${m.numbers.length}</b>${L("stat_numbers")}</div>
        <div><b>${m.requirements.length}</b>${L("stat_req")}</div>
      </div>
    </div>
    <div class="map-grid">
      <section class="panel"><h4>${icon("calendar")}${L("timeline")}<span class="cnt">${m.timeline.length}</span></h4>
        ${m.timeline.length ? `<ul class="timeline">${m.timeline.map((t) => `<li><div class="date">${esc(t.date || "")}</div><div class="ev">${esc(t.event || "")}${locLink(t)}</div></li>`).join("")}</ul>` : none}
      </section>
      <section class="panel"><h4>${icon("hash")}${L("numbers")}<span class="cnt">${m.numbers.length}</span></h4>
        ${m.numbers.length ? `<div class="tiles">${m.numbers.map((n) => `<div class="tile"><div class="v">${esc(n.value || "")}</div><div class="l">${esc(n.label || "")}</div><div>${locLink(n)}</div></div>`).join("")}</div>` : none}
      </section>
      <section class="panel wide"><h4>${icon("check")}${L("requirements")}<span class="cnt" id="reqCount">${reqDone}/${m.requirements.length} ${L("done_of")}</span></h4>
        ${m.requirements.length ? `<div class="progress"><div id="reqBar" style="width:${m.requirements.length ? (reqDone / m.requirements.length) * 100 : 0}%"></div></div>
        <ul class="checklist">${m.requirements.map((r, i) => `<li class="${done.includes(i) ? "done" : ""}"><input type="checkbox" data-i="${i}" ${done.includes(i) ? "checked" : ""}><span class="txt">${esc(r.text || "")}</span>${locLink(r)}</li>`).join("")}</ul>` : none}
      </section>
      ${m.terms.length ? `<section class="panel wide"><h4>${icon("book")}${L("terms")}<span class="cnt">${m.terms.length}</span></h4>
        <dl class="terms">${m.terms.map((t) => `<div><dt>${esc(t.term || "")}</dt><dd>${esc(t.definition || "")}</dd></div>`).join("")}</dl></section>` : ""}
    </div>`;
  $("#mapBody").querySelectorAll(".checklist input").forEach((box) => {
    box.onchange = () => {
      const i = +box.dataset.i;
      done = box.checked ? [...new Set([...done, i])] : done.filter((x) => x !== i);
      try { localStorage.setItem(checklistKey(doc), JSON.stringify(done)); } catch (_) {}
      box.closest("li").classList.toggle("done", box.checked);
      const count = m.requirements.filter((_, k) => done.includes(k)).length;
      $("#reqCount").textContent = `${count}/${m.requirements.length} ${L("done_of")}`;
      $("#reqBar").style.width = `${(count / m.requirements.length) * 100}%`;
    };
  });
}

/* ---------- сравнение версий ---------- */
function renderCompare() {
  const pick = $("#cmpPick"), body = $("#cmpBody");
  if (state.docs.length < 2) {
    pick.innerHTML = "";
    body.innerHTML = `<button type="button" class="empty-state" data-upload><div class="big">${icon("compare")}</div><b>${L("cmp_need")}</b></button>`;
    return;
  }
  const has = (id) => state.docs.some((d) => d.id === id);
  if (!has(state.cmpB)) state.cmpB = state.docs[state.docs.length - 1].id;
  if (!has(state.cmpA) || state.cmpA === state.cmpB) state.cmpA = state.docs.find((d) => d.id !== state.cmpB).id;
  const options = (sel) => state.docs.map((d) => `<option value="${d.id}" ${d.id === sel ? "selected" : ""}>${esc(d.name)}</option>`).join("");
  pick.innerHTML = `
    <label><span>${L("cmp_old")}</span><select id="cmpA">${options(state.cmpA)}</select></label>
    <button type="button" class="icon-btn" id="cmpSwap" aria-label="swap">${icon("swap")}</button>
    <label><span>${L("cmp_new")}</span><select id="cmpB">${options(state.cmpB)}</select></label>
    <button type="button" class="btn" id="cmpGo">${L("cmp_go")}</button>`;
  $("#cmpA").onchange = (e) => { state.cmpA = e.target.value; };
  $("#cmpB").onchange = (e) => { state.cmpB = e.target.value; };
  $("#cmpSwap").onclick = () => { [state.cmpA, state.cmpB] = [state.cmpB, state.cmpA]; renderCompare(); };
  $("#cmpGo").onclick = runCompare;
  const r = state.cmp;
  if (r && r.a.id === state.cmpA && r.b.id === state.cmpB && r.lang === state.lang) paintCompare(r);
  else if (!r || !r.loading) body.innerHTML = "";
}

async function runCompare() {
  if (state.cmpA === state.cmpB) return toast(L("cmp_pick2"), true);
  const a = state.cmpA, b = state.cmpB, lang = state.lang;
  state.cmp = { loading: true, a: { id: a }, b: { id: b }, lang };
  $("#cmpBody").innerHTML = stagedState("compare");
  try {
    const data = await api(`/api/compare?a=${a}&b=${b}&lang=${lang}`);
    state.cmp = { ...data, lang };
  } catch (e) {
    state.cmp = null;
    $("#cmpBody").innerHTML = `<div class="empty-state">${L("error")}: ${esc(e.message)}</div>`;
    return;
  }
  if (state.view === "compare") renderCompare();
}

function paintCompare(r) {
  const st = r.stats;
  const list = (items, cls) => items.length ? `<ul class="${cls}">${items.map((x) => `<li>${esc(x)}</li>`).join("")}</ul>` : "";
  const sm = r.summary;
  const words = (parts) => parts.map(([op, t]) => op === "eq" ? esc(t) : `<${op}>${esc(t)}</${op}>`).join("");
  const change = (c) => {
    const loc = esc(c.loc_new || c.loc_old || "");
    const text = c.kind === "changed" ? words(c.words) : c.kind === "added" ? `<ins>${esc(c.new)}</ins>` : `<del>${esc(c.old)}</del>`;
    return `<div class="cmp-item ${c.kind}"><div class="cmp-tag"><b>${L("cmp_" + c.kind)}</b>${loc ? `<span>${loc}</span>` : ""}</div><div class="cmp-text">${text}</div></div>`;
  };
  if (!r.changes.length) {
    $("#cmpBody").innerHTML = `<div class="map-hero"><h3>${icon("check")} ${L("cmp_same")}</h3><p>${esc(r.a.name)} · ${esc(r.b.name)}</p></div>`;
    return;
  }
  $("#cmpBody").innerHTML = `
    <div class="map-hero">
      <h3>${esc(r.a.name)} → ${esc(r.b.name)}</h3>
      ${sm ? `<p>${esc(sm.verdict)}</p>` : ""}
      <div class="map-stats cmp-stats">
        <div class="add"><b>+${st.added}</b>${L("cmp_added")}</div>
        <div class="del"><b>−${st.removed}</b>${L("cmp_removed")}</div>
        <div class="chg"><b>${st.changed}</b>${L("cmp_changed")}</div>
        <div><b>${st.similarity}%</b>${L("cmp_similar")}</div>
      </div>
    </div>
    ${sm && (sm.points.length || sm.attention.length) ? `<div class="cmp-summary">
      ${sm.points.length ? `<div class="panel"><h4>${icon("spark")}${L("cmp_points")}</h4>${list(sm.points, "cmp-points")}</div>` : ""}
      ${sm.attention.length ? `<div class="panel warn"><h4>${icon("pin")}${L("cmp_attention")}</h4>${list(sm.attention, "cmp-points")}</div>` : ""}
    </div>` : ""}
    <div class="cmp-head"><h4 class="cmp-h">${L("cmp_all")} · ${st.total}</h4>
      <div class="cmp-export"><span>${L("export_as")}:</span><button type="button" class="btn ghost" data-fmt="pdf">PDF</button><button type="button" class="btn ghost" data-fmt="docx">Word</button></div></div>
    <div class="cmp-list">${r.changes.map(change).join("")}</div>
    ${r.truncated ? `<p class="muted">${L("cmp_trunc")}</p>` : ""}`;
  $("#cmpBody").querySelectorAll("[data-fmt]").forEach((b) => (b.onclick = () =>
    downloadExport({ format: b.dataset.fmt, kind: "compare", a: r.a.id, b: r.b.id })));
}

/* ---------- проверка знаний ---------- */
function renderQuizMode() {
  const box = $("#quizMode");
  box.innerHTML = [["quiz", L("mode_quiz")], ["cards", L("mode_cards")]].map(([k, label]) =>
    `<button type="button" data-mode="${k}" class="${state.quizMode === k ? "active" : ""}">${label}</button>`).join("");
  box.querySelectorAll("button").forEach((b) => (b.onclick = () => { state.quizMode = b.dataset.mode; renderQuiz(); }));
}

function renderQuiz() {
  renderQuizMode();
  renderPicker("#quizPicker", "quizDoc", () => { state.quiz = null; state.cards = null; renderQuiz(); });
  const body = $("#quizBody");
  const doc = currentDoc("quizDoc");
  if (!doc) { body.innerHTML = emptyState(); return; }
  if (state.quizMode === "cards") return renderCards(doc);
  const qz = state.quiz && state.quiz.docId === doc.id ? state.quiz : null;
  if (!qz) return paintQuizStart(doc);
  if (qz.loading) { body.innerHTML = stagedState("quiz"); return; }
  if (qz.i >= qz.questions.length) return paintQuizResult(doc, qz);
  paintQuestion(qz);
}

function paintQuizStart(doc) {
  $("#quizBody").innerHTML = `
    <div class="quiz-start">
      <div class="big">${icon("quiz")}</div>
      <h3>${esc(doc.name)}</h3>
      <div class="muted">${L("quiz_intro")} · ${L("quiz_new_note")}</div>
      <div class="seg">${[5, 7, 10].map((n) => `<button type="button" data-n="${n}" class="${n === state.quizN ? "active" : ""}">${n}</button>`).join("")}</div>
      <div><button class="btn" id="quizGo">${L("quiz_start")}</button></div>
    </div>`;
  $("#quizBody").querySelectorAll(".seg button").forEach((b) => (b.onclick = () => { state.quizN = +b.dataset.n; paintQuizStart(doc); }));
  $("#quizGo").onclick = () => startQuiz(doc);
}

async function startQuiz(doc) {
  state.quiz = { docId: doc.id, loading: true, questions: [], i: 0, answers: [] };
  renderQuiz();
  try {
    const data = await api(`/api/documents/${doc.id}/quiz?lang=${state.lang}&n=${state.quizN}`);
    if (!state.quiz || state.quiz.docId !== doc.id) return;
    state.quiz = { docId: doc.id, loading: false, questions: data.questions || [], i: 0, answers: [] };
    if (!state.quiz.questions.length) { $("#quizBody").innerHTML = `<div class="empty-state">${L("nothing")}</div>`; return; }
  } catch (e) {
    state.quiz = null;
    toast(`${L("error")}: ${e.message}`, true);
  }
  if (state.view === "quiz") renderQuiz();
}

function paintQuestion(qz) {
  const q = qz.questions[qz.i];
  const total = qz.questions.length;
  const answered = qz.answers.length > qz.i;
  $("#quizBody").innerHTML = `
    <div class="q-card">
      <div class="q-top"><span>${L("question")} ${qz.i + 1} / ${total}</span><span>✔ ${qz.answers.filter((a, k) => a === qz.questions[k].answer).length}</span></div>
      <div class="progress"><div style="width:${(qz.i / total) * 100}%"></div></div>
      <div class="q-text">${esc(q.question)}</div>
      <div class="options">${q.options.map((o, k) => `<button type="button" class="option" data-k="${k}"><span class="letter">${"ABCD"[k]}</span><span>${esc(o)}</span></button>`).join("")}</div>
      <div id="qExplain"></div>
      <div class="q-actions" id="qNext"></div>
    </div>`;
  const reveal = (choice) => {
    $("#quizBody").querySelectorAll(".option").forEach((b) => {
      const k = +b.dataset.k;
      b.disabled = true;
      if (k === q.answer) b.classList.add("correct");
      else if (k === choice) b.classList.add("wrong");
    });
    const ok = choice === q.answer;
    $("#qExplain").innerHTML = `<div class="explain"><b style="color:var(${ok ? "--ok" : "--bad"})">${ok ? L("correct") : L("wrong")}</b>${q.explanation ? `<span>${esc(q.explanation)}</span>` : ""}${locLink(q)}</div>`;
    const last = qz.i === total - 1;
    $("#qNext").innerHTML = `<button class="btn" type="button">${last ? L("finish") : L("next")}</button>`;
    $("#qNext button").onclick = () => { qz.i += 1; renderQuiz(); };
  };
  $("#quizBody").querySelectorAll(".option").forEach((b) => (b.onclick = () => {
    qz.answers[qz.i] = +b.dataset.k;
    reveal(+b.dataset.k);
  }));
  if (answered) reveal(qz.answers[qz.i]);
}

function paintQuizResult(doc, qz) {
  const total = qz.questions.length;
  const right = qz.answers.filter((a, k) => a === qz.questions[k].answer).length;
  const pct = Math.round((right / total) * 100);
  const color = pct >= 80 ? "#16a34a" : pct >= 50 ? "#f59e0b" : "#dc2626";
  const msg = pct >= 80 ? L("score_great") : pct >= 50 ? L("score_ok") : L("score_low");
  const r = 64, c = 2 * Math.PI * r;
  const mistakes = qz.questions.map((q, k) => ({ q, a: qz.answers[k] })).filter((x) => x.a !== x.q.answer);
  $("#quizBody").innerHTML = `
    <div class="q-card result">
      <div class="ring"><svg viewBox="0 0 150 150"><circle cx="75" cy="75" r="${r}" fill="none" stroke="var(--panel-2)" stroke-width="12"/>
        <circle cx="75" cy="75" r="${r}" fill="none" stroke="${color}" stroke-width="12" stroke-linecap="round" stroke-dasharray="${c}" stroke-dashoffset="${c * (1 - right / total)}"/></svg>
        <div class="pct" style="color:${color}">${pct}%</div></div>
      <h3>${msg}</h3>
      <div class="muted">${right} / ${total} · ${esc(doc.name)}</div>
      ${mistakes.length ? `<div class="mistakes"><b style="color:var(--text)">${L("your_mistakes")}</b>${mistakes.map((x) => `<div>${esc(x.q.question)}<br><b>${L("correct_answer")}: ${esc(x.q.options[x.q.answer])}</b>${locLink(x.q)}</div>`).join("")}</div>` : ""}
      <div class="q-actions" style="justify-content:center;gap:8px">
        ${mistakes.length ? `<button class="btn ghost" type="button" id="qRetry">${L("fix_mistakes")} · ${mistakes.length}</button>` : ""}
        <button class="btn" type="button" id="qNew">${L("new_quiz")}</button>
      </div>
    </div>`;
  // всё верно — повторять те же вопросы незачем; с ошибками — пересдаём только ошибки
  if (mistakes.length) $("#qRetry").onclick = () => {
    qz.questions = mistakes.map((x) => x.q);
    qz.i = 0;
    qz.answers = [];
    renderQuiz();
  };
  $("#qNew").onclick = () => startQuiz(doc);
}

/* ---------- карточки для запоминания ---------- */
function renderCards(doc) {
  const body = $("#quizBody");
  const cs = state.cards && state.cards.docId === doc.id ? state.cards : null;
  if (!cs) {
    body.innerHTML = `
      <div class="quiz-start">
        <div class="big">${icon("book")}</div>
        <h3>${esc(doc.name)}</h3>
        <div class="muted">${L("cards_intro")}</div>
        <div class="seg">${[6, 10, 15].map((n) => `<button type="button" data-n="${n}" class="${n === state.cardsN ? "active" : ""}">${n}</button>`).join("")}</div>
        <div><button class="btn" id="cardsGo">${L("cards_start")}</button></div>
      </div>`;
    body.querySelectorAll(".seg button").forEach((b) => (b.onclick = () => { state.cardsN = +b.dataset.n; renderCards(doc); }));
    $("#cardsGo").onclick = () => startCards(doc);
    return;
  }
  if (cs.loading) { body.innerHTML = stagedState("cards"); return; }
  if (!cs.queue.length) return paintCardsDone(doc, cs);
  const card = cs.cards[cs.queue[0]];
  const done = Math.max(0, cs.total - new Set(cs.queue).size);
  body.innerHTML = `
    <div class="fc-wrap">
      <div class="q-top"><span>${L("card_n")} ${Math.min(done + 1, cs.total)} / ${cs.total}</span><span>${cs.queue.length} ${L("left")}</span></div>
      <div class="progress"><div style="width:${(done / cs.total) * 100}%"></div></div>
      <button type="button" class="fc ${cs.flipped ? "flipped" : ""}" id="fcCard" aria-live="polite">
        <span class="fc-inner">
          <span class="fc-face fc-front"><b>${esc(card.front)}</b><small>${L("flip")}</small></span>
          <span class="fc-face fc-back"><b>${esc(card.back)}</b>${card.quote ? `<small>«${esc(card.quote)}»</small>` : ""}</span>
        </span>
      </button>
      <div class="fc-actions" ${cs.flipped ? "" : "hidden"}>
        ${locLink(card)}
        <span class="spacer"></span>
        <button type="button" class="btn ghost" id="fcAgain">${L("again")}</button>
        <button type="button" class="btn" id="fcKnow">${L("know")}</button>
      </div>
    </div>`;
  $("#fcCard").onclick = () => { cs.flipped = !cs.flipped; renderCards(doc); };
  const next = (known) => {
    const i = cs.queue.shift();
    if (known) { if (!cs.missed.has(i)) cs.knownFirst += 1; }
    else { cs.missed.add(i); cs.queue.push(i); }
    cs.flipped = false;
    renderCards(doc);
  };
  if (cs.flipped) {
    $("#fcAgain").onclick = () => next(false);
    $("#fcKnow").onclick = () => next(true);
  }
}

async function startCards(doc) {
  state.cards = { docId: doc.id, loading: true };
  renderQuiz();
  try {
    const data = await api(`/api/documents/${doc.id}/cards?lang=${state.lang}&n=${state.cardsN}`);
    if (!state.cards || state.cards.docId !== doc.id) return;
    const cards = data.cards || [];
    if (!cards.length) { state.cards = null; $("#quizBody").innerHTML = `<div class="empty-state">${L("nothing")}</div>`; return; }
    state.cards = { docId: doc.id, cards, queue: cards.map((_, i) => i), total: cards.length, missed: new Set(), knownFirst: 0, flipped: false };
  } catch (e) {
    state.cards = null;
    toast(`${L("error")}: ${e.message}`, true);
  }
  if (state.view === "quiz" && state.quizMode === "cards") renderQuiz();
}

function paintCardsDone(doc, cs) {
  $("#quizBody").innerHTML = `
    <div class="quiz-start">
      <div class="big">${icon("check")}</div>
      <h3>${L("cards_done")}</h3>
      <div class="muted">${L("cards_stat").replace("{k}", cs.knownFirst).replace("{n}", cs.total)} · ${esc(doc.name)}</div>
      <div class="q-actions" style="justify-content:center;gap:8px">
        ${cs.missed.size ? `<button class="btn ghost" type="button" id="fcRetry">${L("cards_hard")} · ${cs.missed.size}</button>` : ""}
        <button class="btn" type="button" id="fcNew">${L("new_cards")}</button>
      </div>
    </div>`;
  // повторяем только трудные карточки; если все знали сразу — только новые
  if (cs.missed.size) $("#fcRetry").onclick = () => {
    const hard = [...cs.missed];
    Object.assign(cs, { queue: hard, total: hard.length, missed: new Set(), knownFirst: 0, flipped: false });
    renderCards(doc);
  };
  $("#fcNew").onclick = () => startCards(doc);
}

/* ================= пользователь ================= */
// гость видит интерфейс; вопрос, загрузка и данные — только после входа
function requireLogin(reason, pendingQuestion) {
  if (pendingQuestion) { try { sessionStorage.setItem("mind_pending_q", pendingQuestion); } catch (_) {} }
  if (document.querySelector(".confirm")) return;
  const text = { ask: L("gate_ask"), upload: L("gate_upload") }[reason] || L("gate_any");
  const wrap = document.createElement("div");
  wrap.className = "confirm";
  wrap.innerHTML = `<div class="confirm-card" role="dialog" aria-modal="true">
    <h3>${esc(L("gate_t"))}</h3><p>${esc(text)}</p>
    <div class="row-actions"><button type="button" class="btn ghost" data-go="later">${L("later")}</button>
    <button type="button" class="btn ghost" data-go="register">${L("sign_up")}</button>
    <button type="button" class="btn" data-go="login">${L("sign_in")}</button></div></div>`;
  wrap.addEventListener("click", (e) => {
    const b = e.target.closest("[data-go]");
    if (b && b.dataset.go !== "later") { location.href = b.dataset.go === "register" ? "/login?mode=register" : "/login"; return; }
    if (b || e.target === wrap) wrap.remove();
  });
  document.body.appendChild(wrap);
  wrap.querySelector('[data-go="login"]').focus();
}

function renderUser() {
  const u = state.user;
  if (state.anon) {
    $("#userAvatar").textContent = "?";
    $("#userName").innerHTML = `${L("anon")}<small>${L("anon_hint")}</small>`;
    return;
  }
  if (!u) return;
  $("#userAvatar").textContent = (u.guest ? "G" : (u.name || "?").trim()[0]) || "?";
  $("#userName").innerHTML = u.guest ? `${L("guest")}<small>${L("settings")}</small>` : `${esc(u.name)}<small>${esc(u.email)}</small>`;
}

async function logout() {
  await fetch("/api/auth/logout", { method: "POST" });
  location.href = "/login";
}

/* ================= настройки ================= */
const DEFAULT_PREFS = {
  theme: "system", accent: "indigo", font: "m", width: "normal", ui_lang: "auto", answer_lang: "auto",
  answer_style: "balanced", answer_model: "lite", show_sources: true, show_trust: true, suggestions: true,
};
function guestPrefs() {
  try { return JSON.parse(localStorage.getItem("mind_guest_prefs") || "{}"); } catch (_) { return {}; }
}
const prefs = () => ({ ...DEFAULT_PREFS, ...(state.user ? state.user.settings || {} : guestPrefs()) });
const jsonPost = (path, body, method = "POST") =>
  api(path, { method, headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });

function setLang(lang) {
  state.lang = lang === "auto" ? navLang() : lang;
  try { localStorage.setItem("mind_lang", state.lang); } catch (_) {}
  applyI18n();
}

function navLang() {
  const nav = (navigator.language || "kk").slice(0, 2);
  return nav === "ru" ? "ru" : nav === "en" ? "en" : "kk";
}

function applyPrefs() {
  const p = prefs(), root = document.documentElement;
  if (p.theme === "system") delete root.dataset.theme; else root.dataset.theme = p.theme;
  root.dataset.accent = p.accent;
  delete root.dataset.font;
  if ($("#modelLabel")) renderModelPicker();  // «Размер текста» временно отключён: увеличение ломало окно настроек
  root.dataset.width = p.width;
  try { localStorage.setItem("mind_prefs", JSON.stringify({ theme: p.theme, accent: p.accent, font: p.font, width: p.width })); } catch (_) {}
  if (p.ui_lang !== "auto" && p.ui_lang !== state.lang) setLang(p.ui_lang);
}

async function savePrefs(patch) {
  if (!state.user) {  // гость: настройки хранятся в браузере, после входа переносятся в аккаунт
    try { localStorage.setItem("mind_guest_prefs", JSON.stringify({ ...guestPrefs(), ...patch })); } catch (_) {}
    applyPrefs();
    if ("ui_lang" in patch) setLang(patch.ui_lang);
    renderSettings();
    return;
  }
  state.user.settings = { ...prefs(), ...patch };
  applyPrefs();
  if ("ui_lang" in patch) setLang(patch.ui_lang);
  renderSettings();
  try { state.user.settings = await jsonPost("/api/settings", patch, "PUT"); } catch (_) { toast(L("error"), true); }
}

function openSettings(tab) {
  if (tab) state.setTab = tab;
  $("#settings").hidden = false;
  renderSettings();
}

function closeSettings() { $("#settings").hidden = true; }

function errText(e) {
  let code = "";
  try { code = JSON.parse(e.message).detail; } catch (_) {}
  return L("err_" + code) !== "err_" + code ? L("err_" + code) : L("error");
}

// ---- строительные блоки разметки
const segRow = (key, title, desc, options) => `
  <div class="set-row"><div class="lbl"><b>${title}</b>${desc ? `<span>${desc}</span>` : ""}</div>
    <div class="seg">${options.map(([v, label]) => `<button type="button" data-pref="${key}" data-val="${v}" class="${prefs()[key] === v ? "active" : ""}">${label}</button>`).join("")}</div></div>`;
const toggleRow = (key, title, desc) => `
  <div class="set-row"><div class="lbl"><b>${title}</b><span>${desc}</span></div>
    <label class="switch"><input type="checkbox" data-toggle="${key}" ${prefs()[key] ? "checked" : ""}><i></i></label></div>`;
const actionRow = (act, title, desc, label, cls = "ghost") => `
  <div class="set-row"><div class="lbl"><b>${title}</b><span>${desc}</span></div>
    <button type="button" class="btn ${cls}" data-act="${act}">${label}</button></div>`;
const head = (tab) => `<h2>${L("set_" + tab)}</h2><p class="sub">${L(tab + "_sub")}</p>`;

const ACCENTS = { graphite: "#3f3f46", indigo: "#6366f1", emerald: "#10a26b", ocean: "#0e8fd6", amber: "#d4880f", rose: "#e0466a" };

const gateBlock = (key) => `<div class="set-group"><div class="set-row"><div class="lbl"><b>${L("gate_t")}</b><span>${L(key)}</span></div>
  <div class="row-actions"><a class="btn ghost" href="/login?mode=register">${L("sign_up")}</a><a class="btn" href="/login">${L("sign_in")}</a></div></div></div>`;

const TABS = {
  profile() {
    if (state.anon) return head("profile") + gateBlock("gate_profile");
    const u = state.user || {};
    return head("profile") + `
      <div class="set-group"><div class="set-row">
        <span class="avatar-u" style="width:52px;height:52px;font-size:20px">${esc(u.guest ? "G" : (u.name || "?")[0])}</span>
        <div class="lbl"><b>${esc(u.guest ? L("guest") : u.name || "")}</b><span>${esc(u.email || "")}</span></div></div></div>
      ${u.guest ? `<div class="set-group"><div class="set-row"><div class="lbl"><span>${L("guest_note")}</span></div>
        <button type="button" class="btn" data-act="logout">${L("logout")}</button></div></div>` : `
      <div class="set-group" style="padding:16px">
        <div class="field"><label>${L("name")}</label><input class="input" id="pfName" maxlength="60" value="${esc(u.name || "")}"></div>
        <div class="field"><label>${L("email")}</label><input class="input" value="${esc(u.email || "")}" disabled></div>
        <button type="button" class="btn" data-act="save-name">${L("save")}</button></div>`}`;
  },
  appearance() {
    const p = prefs();
    return head("appearance") + `
      <div class="set-group"><div class="set-row" style="padding-bottom:0"><div class="lbl"><b>${L("theme")}</b></div></div>
        <div class="theme-cards">${["system", "light", "dark", "sepia", "midnight"].map((t) => `
          <button type="button" class="theme-card ${p.theme === t ? "active" : ""}" data-pref="theme" data-val="${t}"><div class="pv ${t}"></div>${L("theme_" + t)}</button>`).join("")}</div>
        <div class="set-row"><div class="lbl"><b>${L("accent")}</b><span>${L("accent_d")}</span></div>
          <div class="accents">${Object.entries(ACCENTS).map(([k, c]) => `
            <button type="button" title="${L("ac_" + k)}" aria-label="${L("ac_" + k)}" data-pref="accent" data-val="${k}" class="${p.accent === k ? "active" : ""}" style="background:${c}"></button>`).join("")}</div></div></div>
      <div class="set-group">
        ${segRow("width", L("width"), L("width_d"), [["normal", L("w_normal")], ["wide", L("w_wide")]])}</div>`;
  },
  language() {
    const opts = [["auto", L("auto")], ["kk", "Қазақша"], ["ru", "Русский"], ["en", "English"]];
    return head("language") + `<div class="set-group">
      ${segRow("ui_lang", L("ui_lang"), L("ui_lang_d"), opts)}</div>`;
  },
  ai() {
    return head("ai") + `<div class="set-group">
      ${segRow("answer_style", L("style"), L("style_d"), [["concise", L("st_concise")], ["balanced", L("st_balanced")], ["detailed", L("st_detailed")]])}</div>
      <div class="set-group">
      ${toggleRow("show_sources", L("show_sources"), L("show_sources_d"))}
      ${toggleRow("show_trust", L("show_trust"), L("show_trust_d"))}
      ${toggleRow("suggestions", L("suggestions"), L("suggestions_d"))}</div>`;
  },
  plan() {
    const pro = hasPro();
    const list = (key) => `<ul>${L(key).map((f) => `<li>${icon("tick")}<span>${esc(f)}</span></li>`).join("")}</ul>`;
    return head("plan") + `<div class="plans">
      <div class="plan ${pro ? "" : "current"}">
        <div class="plan-top"><b>${L("lite")}</b>${pro ? "" : `<span class="mm-badge">${L("plan_current")}</span>`}</div>
        <div class="plan-price">${L("plan_free_price")}</div>
        ${list("lite_f")}
      </div>
      <div class="plan pro ${pro ? "current" : ""}">
        <div class="plan-top"><b>${L("pro")}</b><span class="mm-badge pro">${pro ? L("plan_current") : "PRO · " + L("soon")}</span></div>
        <div class="plan-price">${L("plan_pro_price")}</div>
        <div class="plan-plus">${L("plan_plus")}</div>
        ${list("pro_f")}
        ${pro ? "" : `<button type="button" class="btn" disabled>${L("plan_soon")}</button>`}
      </div></div>`;
  },
  data() {
    if (state.anon) return head("data") + gateBlock("gate_data");
    return head("data") + `
      <div class="set-group"><div class="set-row"><div class="lbl"><b>${L("docs_count")}</b></div>
        <span style="font-family:var(--display);font-size:22px;font-weight:700">${state.docs.length}</span></div></div>
      <div class="set-group">
        ${actionRow("export", L("export"), L("export_d"), icon("download") + " " + L("export"))}
        ${actionRow("clear-history", L("clear_hist"), L("clear_hist_d"), L("delete"), "danger")}</div>
      <div class="set-group danger-zone">${actionRow("delete-docs", L("delete_docs"), L("delete_docs_d"), L("delete"), "danger")}</div>`;
  },
  system() {
    const s = state.status || {};
    const ocrLangs = (s.ocr || "").startsWith("tesseract:") ? s.ocr.split(":")[1].split("+") : [];
    const langName = { kaz: "ҚАЗ", rus: "РУС", eng: "ENG" };
    const llm = !s.llm_enabled ? `<span class="pill">${L("offline")}</span>`
      : s.llm_ok === false ? `<span class="pill bad"><i></i>${L("disconnected")}</span>`
      : s.llm_ok ? `<span class="pill ok"><i></i>${L("connected")}</span>` : `<span class="pill">…</span>`;
    return head("system") + `<div class="sys-grid">
      <div class="sys-card"><div class="k">${icon("spark")}${L("model")}</div>
        <div class="v">${esc(s.llm_model || "—")}</div>${llm}
        <div style="margin-top:12px"><button type="button" class="btn ghost" data-act="check-llm">${L("check")}</button></div></div>
      <div class="sys-card"><div class="k">${icon("scan")}${L("ocr_card")}</div>
        <div class="v">${ocrLangs.length ? "Tesseract" : L("ocr_none")}</div>
        ${ocrLangs.map((x) => `<span class="pill ok"><i></i>${langName[x] || x}</span>`).join("")}</div>
      <div class="sys-card"><div class="k">${icon("chat")}${L("telegram")}</div>
        <div class="v">${s.telegram ? L("tg_on") : L("tg_off")}</div>
        <span class="pill ${s.telegram ? "ok" : ""}"><i></i>Telegram</span></div>
      <div class="sys-card"><div class="k">${icon("file")}${L("formats")}</div>
        <div class="v">Mind AI ${esc(s.version || "")}</div>
        <div>${(s.formats || []).filter((f) => [".pdf", ".docx", ".pptx", ".xlsx", ".csv", ".txt", ".html", ".jpg", ".png", ".doc", ".rtf"].includes(f))
          .map((f) => `<span class="pill">${f.slice(1).toUpperCase()}</span>`).join("")}</div></div></div>`;
  },
  account() {
    if (state.anon) return head("account") + gateBlock("gate_account");
    const u = state.user || {};
    return head("account") + (u.guest || u.provider === "firebase" ? "" : `
      <div class="set-group" style="padding:16px"><b style="display:block;margin-bottom:12px">${L("change_pw")}</b>
        <div class="field"><label>${L("old_pw")}</label><input class="input" type="password" id="pwOld" autocomplete="current-password"></div>
        <div class="field"><label>${L("new_pw")}</label><input class="input" type="password" id="pwNew" autocomplete="new-password">
          <span style="font-size:12px;color:var(--muted)">${L("pw_rule")}</span></div>
        <button type="button" class="btn" data-act="change-pw">${L("save")}</button></div>`) + `
      <div class="set-group">${actionRow("logout", L("logout"), L("logout_d"), icon("logout") + " " + L("logout"))}</div>
      <div class="set-group danger-zone">${actionRow("delete-account", L("delete_acc"), L("delete_acc_d"), L("delete"), "danger")}</div>`;
  },
};

function renderSettings() {
  if ((!state.user && !state.anon) || $("#settings").hidden) return;
  document.querySelectorAll("#setNav button").forEach((b) => b.classList.toggle("active", b.dataset.tab === state.setTab));
  $("#setBody").innerHTML = TABS[state.setTab]();
}

function exportChat() {
  const lines = [`# Mind AI — ${new Date().toLocaleString()}`, ""];
  for (const m of state.log) {
    lines.push(m.role === "user" ? `**${L("you")}:** ${m.text}` : `**Mind AI:** ${m.text}`);
    if (m.sources && m.sources.length) lines.push("", ...m.sources.map((x) => `> [${x.n}] ${x.doc_name}${x.loc_label ? ", " + x.loc_label : ""}`));
    lines.push("");
  }
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([lines.join("\n")], { type: "text/markdown" }));
  a.download = `mind-ai-chat-${new Date().toISOString().slice(0, 10)}.md`;
  a.click();
  URL.revokeObjectURL(a.href);
}

const ACTIONS = {
  async "save-name"() {
    try { state.user = await jsonPost("/api/profile", { name: $("#pfName").value }, "PUT"); renderUser(); renderSettings(); toast(L("saved")); }
    catch (e) { toast(errText(e), true); }
  },
  export: exportChat,
  async "clear-history"() {
    if (!(await confirmDialog(L("del_all_chats_t"), L("irreversible")))) return;
    await api("/api/chats", { method: "DELETE" });
    newChat();
    await loadChats();
    toast(L("done"));
  },
  async "delete-docs"() {
    if (!(await confirmDialog(L("del_all_docs_t"), L("irreversible")))) return;
    await api("/api/documents", { method: "DELETE" });
    state.selected.clear();
    state.mapCache = {};
    state.quiz = null;
    await loadDocs();
    renderSettings();
    toast(L("done"));
  },
  async "check-llm"(btn) {
    btn.textContent = L("checking");
    const c = await api("/api/llm-check").catch(() => ({ ok: false }));
    state.status.llm_ok = c.ok;
    renderSettings();
  },
  async "change-pw"() {
    try {
      await jsonPost("/api/profile/password", { old: $("#pwOld").value, new: $("#pwNew").value });
      toast(L("pw_changed"));
      renderSettings();
    } catch (e) { toast(errText(e), true); }
  },
  logout,
  async "delete-account"() {
    if (!(await confirmDialog(L("del_acc_t"), L("delete_acc_d")))) return;
    const needPw = !state.user.guest && state.user.provider !== "firebase";  // у входа через Firebase/Google нет пароля здесь
    const password = needPw ? prompt(L("confirm_pw")) || "" : "";
    if (needPw && !password) return;
    try { await jsonPost("/api/profile/delete", { password }); location.href = "/login"; }
    catch (e) { toast(errText(e), true); }
  },
};

function bindSettings() {
  const body = $("#setBody");
  body.addEventListener("click", (e) => {
    const pref = e.target.closest("[data-pref]");
    if (pref) return savePrefs({ [pref.dataset.pref]: pref.dataset.val });
    const act = e.target.closest("[data-act]");
    if (act && ACTIONS[act.dataset.act]) ACTIONS[act.dataset.act](act);
  });
  body.addEventListener("change", (e) => {
    const t = e.target.closest("[data-toggle]");
    if (t) savePrefs({ [t.dataset.toggle]: t.checked });
  });
}

/* ================= сохранённые чаты ================= */
function confirmDialog(title, text, okLabel) {
  return new Promise((resolve) => {
    const wrap = document.createElement("div");
    wrap.className = "confirm";
    wrap.innerHTML = `<div class="confirm-card" role="alertdialog" aria-modal="true">
      <h3>${esc(title)}</h3><p>${esc(text || "")}</p>
      <div class="row-actions"><button type="button" class="btn ghost" data-r="0">${L("cancel")}</button>
      <button type="button" class="btn danger" data-r="1">${esc(okLabel || L("delete"))}</button></div></div>`;
    const close = (r) => { wrap.remove(); document.removeEventListener("keydown", onKey, true); resolve(r); };
    const onKey = (e) => { if (e.key === "Escape") { e.stopPropagation(); close(false); } if (e.key === "Enter") close(true); };
    wrap.addEventListener("click", (e) => { const b = e.target.closest("[data-r]"); if (b) close(b.dataset.r === "1"); else if (e.target === wrap) close(false); });
    document.addEventListener("keydown", onKey, true);
    document.body.appendChild(wrap);
    wrap.querySelector('[data-r="1"]').focus();
  });
}

function timeLabel(ts) {
  const d = new Date(ts * 1000), now = new Date();
  const locale = { kk: "kk-KZ", ru: "ru-RU", en: "en-US" }[state.lang];
  return d.toDateString() === now.toDateString()
    ? d.toLocaleTimeString(locale, { hour: "2-digit", minute: "2-digit" })
    : d.toLocaleDateString(locale, { day: "numeric", month: "short" });
}

function renderChats() {
  const list = $("#chatList");
  list.innerHTML = "";
  for (const c of state.chats) {
    const el = document.createElement("div");
    el.className = "chat-item" + (c.id === state.chatId ? " active" : "");
    el.innerHTML = `<div class="ct"><b>${esc(c.title || L("untitled"))}</b><small>${timeLabel(c.updated)}</small></div>
      <button type="button" class="del" title="${L("delete")}" aria-label="${L("delete")}">${icon("trash")}</button>`;
    el.onclick = (e) => { if (!e.target.closest(".del")) openChat(c.id); };
    el.querySelector(".del").onclick = () => deleteChat(c);
    list.appendChild(el);
  }
  $("#chatCount").textContent = state.chats.length;
  $("#chatEmpty").style.display = state.chats.length ? "none" : "block";
}

async function loadChats() {
  try { state.chats = await api("/api/chats"); } catch (_) { state.chats = []; }
  renderChats();
}

function resetChatView() {
  $("#messages").innerHTML = "";
  $("#suggestions").innerHTML = "";
  $("#welcome").style.display = "";
  state.log = [];
}

function newChat() {
  state.chatId = null;
  resetChatView();
  renderChats();
  setView("chat");
  $("#question").focus();
}

// Рисует диалог заново — при открытии чата и при смене языка (подписи «Копировать», «стр.» и т.п.)
function renderLog(log) {
  resetChatView();
  if (!log.length) return;
  hideWelcome();
  let lastQuestion = "";
  log.forEach((m, i) => {
    if (m.role === "user") {
      addUserMessage(m.text);
      lastQuestion = m.text;
    } else {
      const { body } = addBotMessage();
      body.querySelector(".bubble").innerHTML = md(m.text);
      if (m.vision && m.vision.length) addVisionNote(body, m.vision);
      const sources = m.sources || [];
      renderSources(body, sources, sources.map((x) => x.n), lastQuestion + " " + m.text.slice(0, 300));
      addTools(body, m, lastQuestion);
      if (i === log.length - 1 && m.followups) addFollowups(body, m.followups);
    }
    state.log.push(m);
  });
}

async function openChat(id) {
  if (state.busy) return;
  const chat = await api(`/api/chats/${id}`).catch(() => null);
  if (!chat) { await loadChats(); return; }
  state.chatId = id;
  renderLog(chat.messages.map((m) => ({ role: m.role, text: m.text, sources: m.sources, vision: m.vision, followups: m.followups })));
  renderChats();
  setView("chat");
  scrollDown();
}

async function deleteChat(c) {
  if (!(await confirmDialog(L("del_chat_t"), L("del_chat_d").replace("{t}", c.title || L("untitled"))))) return;
  await api(`/api/chats/${c.id}`, { method: "DELETE" }).catch(() => {});
  if (c.id === state.chatId) newChat();
  await loadChats();
  toast(L("chat_deleted"));
}

async function clearChat() {
  // кнопка-корзина сверху: удаляет текущий чат (с подтверждением)
  const current = state.chats.find((c) => c.id === state.chatId);
  if (current) return deleteChat(current);
  if (!state.log.length) return;
  if (await confirmDialog(L("del_chat_t"), L("irreversible"))) newChat();
}

/* ================= выбор модели и стиля ответа ================= */
const STYLE_KEYS = { concise: "st_concise", balanced: "st_balanced", detailed: "st_detailed" };

const hasPro = () => !!(state.user && state.user.plan === "pro");

function renderModelPicker() {
  const style = prefs().answer_style;
  const model = hasPro() && prefs().answer_model === "pro" ? "pro" : "lite";
  $("#modelLabel").innerHTML = `${L(model)}<span class="mb-style"> · ${L(STYLE_KEYS[style] || "st_balanced")}</span>`;
  const item = (attrs, title, desc, right, cls = "") =>
    `<button type="button" class="mm-item ${cls}" ${attrs}><span class="mm-t"><b>${title}</b><span class="d">${desc}</span></span>${right}</button>`;
  const check = `<svg class="ok"><use href="#i-check"/></svg>`;
  $("#modelMenu").innerHTML =
    `<div class="mm-head">${L("mm_model")}</div>` +
    item('data-model="lite"', `${L("lite")} <span class="mm-badge">${L("free")}</span>`, L("lite_d"), model === "lite" ? check : "") +
    item('data-model="pro"', `${L("pro")} <span class="mm-badge pro">PRO${hasPro() ? "" : " · " + L("soon")}</span>`, L("pro_d"),
      model === "pro" ? check : "", hasPro() ? "" : "soon") +
    `<div class="mm-sep"></div><div class="mm-head">${L("mm_style")}</div>` +
    Object.entries(STYLE_KEYS).map(([k, label]) =>
      item(`data-style="${k}"`, L(label), L(k + "_d"), k === style ? check : "")).join("");
}

function toggleModelMenu(open) {
  const menu = $("#modelMenu");
  const show = open ?? menu.hidden;
  menu.hidden = !show;
  $("#modelBtn").setAttribute("aria-expanded", String(show));
  if (show) renderModelPicker();
}

function setupModelPicker() {
  renderModelPicker();
  $("#modelBtn").onclick = (e) => { e.stopPropagation(); toggleModelMenu(); };
  $("#modelMenu").onclick = (e) => {
    e.stopPropagation();
    const b = e.target.closest(".mm-item");
    if (!b) return;
    if (b.dataset.model === "pro" && !hasPro()) {  // по подписке, пока недоступна — показываем, что в неё входит
      toggleModelMenu(false);
      toast(L("pro_toast"));
      openSettings("plan");
      return;
    }
    if (b.dataset.model) savePrefs({ answer_model: b.dataset.model });
    if (b.dataset.style) savePrefs({ answer_style: b.dataset.style });
    toggleModelMenu(false);
    renderModelPicker();
  };
  document.addEventListener("click", () => toggleModelMenu(false));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") toggleModelMenu(false); });
}

/* ================= voice ================= */
function setupVoice() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) return;
  const btn = $("#micBtn");
  btn.hidden = false;
  let rec = null;
  btn.onclick = () => {
    if (rec) { rec.stop(); return; }
    rec = new SR();
    rec.lang = { kk: "kk-KZ", ru: "ru-RU", en: "en-US" }[state.lang];
    rec.interimResults = true;
    rec.onresult = (e) => {
      $("#question").value = Array.from(e.results).map((r) => r[0].transcript).join("");
      autosize();
    };
    rec.onend = () => { btn.classList.remove("rec"); rec = null; };
    rec.onerror = () => { btn.classList.remove("rec"); rec = null; };
    btn.classList.add("rec");
    rec.start();
  };
}

/* ================= init ================= */
function autosize() {
  const ta = $("#question");
  ta.style.height = "auto";
  ta.style.height = Math.min(ta.scrollHeight, 180) + "px";
}

function init() {
  applyI18n();
  setupVoice();

  const fileInput = $("#fileInput");
  fileInput.onchange = () => uploadFiles(fileInput.files);
  $("#attachBtn").onclick = () => (state.anon ? requireLogin("upload") : fileInput.click());
  setupModelPicker();
  // гостю — приглашение войти ещё до окна выбора файла
  $("#dropzone").addEventListener("click", (e) => { if (state.anon) { e.preventDefault(); requireLogin("upload"); } });

  // Drag & drop — на всё окно
  const dz = $("#dropzone");
  ["dragenter", "dragover"].forEach((t) => document.addEventListener(t, (e) => { e.preventDefault(); dz.classList.add("drag"); }));
  ["dragleave", "drop"].forEach((t) => document.addEventListener(t, (e) => { e.preventDefault(); if (t === "drop" || !e.relatedTarget) dz.classList.remove("drag"); }));
  document.addEventListener("drop", (e) => { if (e.dataTransfer?.files?.length) uploadFiles(e.dataTransfer.files); });

  const ta = $("#question");
  ta.addEventListener("input", autosize);
  ta.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey && !e.isComposing) { e.preventDefault(); $("#composer").requestSubmit(); }
  });
  $("#composer").onsubmit = (e) => {
    e.preventDefault();
    const q = ta.value;
    ta.value = "";
    autosize();
    ask(q);
  };

  $("#clearChat").onclick = clearChat;
  $("#newChat").onclick = () => { newChat(); $("#sidebar").classList.remove("open"); };

  $("#tabs").onclick = (e) => { const b = e.target.closest("button"); if (b) setView(b.dataset.view); };
  $("#evClose").onclick = closeEvidence;
  $("#scrim").onclick = closeEvidence;
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") { closeEvidence(); closeSettings(); } });
  // ссылки «стр. N» в карте документа и в тесте
  document.addEventListener("click", (e) => {
    const link = e.target.closest(".loc-link");
    if (link) openEvidence(link.dataset.chunk, link.dataset.q);
    if (e.target.closest("[data-upload]")) (state.anon ? requireLogin("upload") : $("#fileInput").click());
  });

  $("#userCard").onclick = () => openSettings(state.anon ? "appearance" : undefined);
  $("#setClose").onclick = closeSettings;
  $("#settings").onclick = (e) => { if (e.target.id === "settings") closeSettings(); };
  $("#setNav").onclick = (e) => { const b = e.target.closest("button"); if (b) { state.setTab = b.dataset.tab; renderSettings(); } };
  bindSettings();
  // вошёл ли пользователь: гостю показываем интерфейс без данных
  fetch("/api/auth/me").then(async (res) => {
    if (!res.ok) { state.anon = true; renderUser(); renderDocs(); renderChats(); applyPrefs(); return; }
    state.user = await res.json();
    // настройки, выбранные гостем до входа, переносим в аккаунт
    const gp = guestPrefs();
    if (Object.keys(gp).length) {
      try { localStorage.removeItem("mind_guest_prefs"); } catch (_) {}
      jsonPost("/api/settings", gp, "PUT").then((st) => { state.user.settings = st; applyPrefs(); }).catch(() => {});
    }
    renderUser();
    applyPrefs();
    loadDocs().catch((e) => toast(e.message, true));
    loadChats();
    let pending = null;  // вопрос, набранный до входа, возвращаем в поле ввода
    try { pending = sessionStorage.getItem("mind_pending_q"); sessionStorage.removeItem("mind_pending_q"); } catch (_) {}
    if (pending) { $("#question").value = pending; autosize(); $("#question").focus(); }
  }).catch(() => {});

  $("#openSidebar").onclick = () => $("#sidebar").classList.add("open");
  $("#closeSidebar").onclick = () => $("#sidebar").classList.remove("open");

  api("/api/status").then((s) => {
    state.status = s;
    // реально проверяем модель; если связи нет — одно уведомление вместо постоянной строки
    if (s.llm_enabled) api("/api/llm-check").then((c) => { s.llm_ok = c.ok; if (!c.ok) toast(L("llm_down"), true); }).catch(() => {});
  }).catch(() => {});
}

init();
