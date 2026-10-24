"use strict";

/* ================= i18n ================= */
const I18N = {
  kk: {
    tagline: "Құжаттар бойынша зияткер көмекші",
    upload_title: "Құжатты жүктеу",
    documents: "Құжаттар",
    no_docs_hint: "Файлды осында сүйреңіз немесе жоғарыдағы аймақты басыңыз",
    clear_chat: "Чатты тазалау",
    welcome_title: "Құжатыңызбен сөйлесіңіз",
    welcome_text: "PDF, DOCX немесе басқа құжатты жүктеңіз — DocMind AI оның мазмұны бойынша сұрақтарға нақты жауап беріп, дереккөзін көрсетеді.",
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
    welcome_title: "Поговорите со своим документом",
    welcome_text: "Загрузите PDF, DOCX или другой документ — DocMind AI ответит на вопросы по его содержанию и покажет точный источник.",
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
    welcome_title: "Chat with your documents",
    welcome_text: "Upload a PDF, DOCX or any other document — DocMind AI answers questions about its content and shows the exact source.",
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
  quiz_sub: "Құжат бойынша тест: нұсқаулықты, ережені немесе оқу материалын қаншалықты меңгергеніңізді тексеріңіз.",
  timeline: "Хронология және мерзімдер", numbers: "Негізгі сандар", requirements: "Талаптар чек-парағы", terms: "Терминдер мен атаулар",
  nothing: "Табылмады", done_of: "орындалды", need_doc: "Алдымен сол жақтан құжат жүктеңіз",
  analyzing: "AI құжатты талдап жатыр…", generating: "Сұрақтар құрастырылуда…",
  quiz_intro: "Сұрақтар саны", quiz_start: "Тестті бастау", question: "Сұрақ", next: "Келесі →", finish: "Нәтижені көру",
  retry: "Қайта тапсыру", new_quiz: "Жаңа сұрақтар", correct: "Дұрыс!", wrong: "Қате",
  score_great: "Керемет! Құжатты жақсы білесіз", score_ok: "Жаман емес — бірақ қайталап шығыңыз", score_low: "Құжатты қайта оқып шығу керек",
  your_mistakes: "Қателерді талдау", correct_answer: "Дұрыс жауап", evidence: "Дәлел",
  trust_ok: "{n} дереккөзбен расталған", trust_none: "Құжатта дәлел табылмады",
  stat_pages: "бет", stat_dates: "мерзім", stat_numbers: "сан", stat_req: "талап", map_btn: "Карта",
});
Object.assign(I18N.ru, {
  tab_chat: "Вопрос-ответ", tab_map: "Карта документа", tab_quiz: "Проверка знаний",
  map_h: "Карта документа",
  map_sub: "AI сам разбирает документ: сроки, ключевые цифры, требования и термины — каждый пункт со ссылкой на страницу.",
  quiz_h: "Проверка знаний",
  quiz_sub: "Тест по документу: проверьте, насколько хорошо усвоены инструкция, регламент или учебный материал.",
  timeline: "Хронология и сроки", numbers: "Ключевые цифры", requirements: "Чек-лист требований", terms: "Термины и понятия",
  nothing: "Не найдено", done_of: "выполнено", need_doc: "Сначала загрузите документ слева",
  analyzing: "AI анализирует документ…", generating: "Составляю вопросы…",
  quiz_intro: "Количество вопросов", quiz_start: "Начать тест", question: "Вопрос", next: "Далее →", finish: "Показать результат",
  retry: "Пройти заново", new_quiz: "Новые вопросы", correct: "Верно!", wrong: "Неверно",
  score_great: "Отлично! Вы хорошо знаете документ", score_ok: "Неплохо — но стоит повторить", score_low: "Документ стоит перечитать",
  your_mistakes: "Разбор ошибок", correct_answer: "Правильный ответ", evidence: "Доказательство",
  trust_ok: "Подтверждено {n} источн.", trust_none: "Подтверждение в документе не найдено",
  stat_pages: "стр.", stat_dates: "сроков", stat_numbers: "цифр", stat_req: "требований", map_btn: "Карта",
});
Object.assign(I18N.en, {
  tab_chat: "Q&A", tab_map: "Document map", tab_quiz: "Knowledge check",
  map_h: "Document map",
  map_sub: "AI breaks the document down for you: deadlines, key numbers, requirements and terms — each linked to its page.",
  quiz_h: "Knowledge check",
  quiz_sub: "A test based on the document: check how well an instruction, regulation or study material has been learned.",
  timeline: "Timeline & deadlines", numbers: "Key numbers", requirements: "Requirements checklist", terms: "Terms & names",
  nothing: "Nothing found", done_of: "done", need_doc: "Upload a document on the left first",
  analyzing: "AI is analyzing the document…", generating: "Generating questions…",
  quiz_intro: "Number of questions", quiz_start: "Start the test", question: "Question", next: "Next →", finish: "See result",
  retry: "Try again", new_quiz: "New questions", correct: "Correct!", wrong: "Wrong",
  score_great: "Excellent! You know this document well", score_ok: "Not bad — worth a review", score_low: "Better re-read the document",
  your_mistakes: "Review of mistakes", correct_answer: "Correct answer", evidence: "Evidence",
  trust_ok: "Backed by {n} source(s)", trust_none: "No supporting evidence found",
  stat_pages: "pages", stat_dates: "dates", stat_numbers: "numbers", stat_req: "requirements", map_btn: "Map",
});

const $ = (s) => document.querySelector(s);
const state = {
  lang: pickLang(),
  sid: sessionId(),
  docs: [],
  selected: new Set(),
  status: null,
  busy: false,
  view: "chat",
  mapDoc: null,
  mapCache: {},
  quizDoc: null,
  quiz: null,
  quizN: 5,
};

function pickLang() {
  try {
    const saved = localStorage.getItem("docmind_lang");
    if (saved && I18N[saved]) return saved;
  } catch (_) {}
  const nav = (navigator.language || "kk").slice(0, 2);
  return nav === "ru" ? "ru" : nav === "en" ? "en" : "kk";
}

function sessionId() {
  try {
    let sid = localStorage.getItem("docmind_sid");
    if (!sid) {
      sid = Array.from(crypto.getRandomValues(new Uint8Array(12)), (b) => b.toString(16).padStart(2, "0")).join("");
      localStorage.setItem("docmind_sid", sid);
    }
    return sid;
  } catch (_) {
    return "anon" + Math.random().toString(36).slice(2, 14);
  }
}

const L = (key) => I18N[state.lang][key] ?? I18N.ru[key] ?? key;

function applyI18n() {
  document.documentElement.lang = state.lang;
  document.querySelectorAll("[data-i18n]").forEach((el) => (el.textContent = L(el.dataset.i18n)));
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => (el.placeholder = L(el.dataset.i18nPlaceholder)));
  document.querySelectorAll("[data-i18n-title]").forEach((el) => (el.title = L(el.dataset.i18nTitle)));
  document.querySelectorAll("#langSwitch button").forEach((b) => b.classList.toggle("active", b.dataset.lang === state.lang));
  renderDocs();
  renderStatus();
  renderScope();
  if (state.view === "map") renderMap();
  if (state.view === "quiz") renderQuiz();
}

/* ================= API ================= */
async function api(path, options = {}) {
  const res = await fetch(path, { ...options, headers: { "X-Session-Id": state.sid, ...(options.headers || {}) } });
  if (!res.ok) throw new Error((await res.text()) || res.statusText);
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
  let url = `/api/documents/${docId}/file?session=${encodeURIComponent(state.sid)}`;
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
        <button data-act="summary">✨ ${L("summary")}</button>
        <button data-act="map">🧭 ${L("map_btn")}</button>
        <button data-act="open" title="${L("open")}">↗</button>
        <button data-act="delete" class="del" title="${L("delete")}">🗑</button>
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
    : `🔎 ${L("scope_all")} (${state.docs.length})`;
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
}

async function uploadFiles(files) {
  if (!files.length) return;
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
  if (!confirm(`${L("confirm_delete")}\n${d.name}`)) return;
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
    bubble.innerHTML = `<p><b>${justUploaded ? "✅ " + L("doc_ready") : "✨ " + L("summary_title")}: ${esc(doc.name)}</b><br><small style="color:var(--muted)">${meta}</small></p>${md(s.summary || "")}`;
    if (s.questions && s.questions.length) {
      const wrap = document.createElement("div");
      wrap.innerHTML = `<p style="margin-top:10px"><b>${L("ask_these")}</b></p><div class="summary-q"></div>`;
      const qs = wrap.querySelector(".summary-q");
      for (const q of s.questions) qs.appendChild(chip(q));
      bubble.appendChild(wrap);
      setSuggestions(s.questions.slice(0, 3));
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

const BOT_AVATAR = `<div class="avatar"><svg viewBox="0 0 32 32"><path d="M9 7h9l5 5v13H9z" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="16" cy="18" r="3" fill="currentColor"/></svg></div>`;

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
  const trust = document.createElement("div");
  trust.className = "trust " + (shown.length ? "ok" : "warn");
  trust.textContent = shown.length ? "✔ " + L("trust_ok").replace("{n}", shown.length) : "⚠ " + L("trust_none");
  body.appendChild(trust);
  if (!shown.length) return;
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
    b.innerHTML = `<span class="n">${s.n}</span><span class="t">📍 ${esc(s.doc_name)}${s.loc_label ? " · " + esc(s.loc_label) : ""}</span>`;
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
  const parts = text.replace(/\n/g, " ").split(/(?<=[.!?…;])\s+/);
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
    $("#evName").textContent = `${info.doc_name}${info.loc_label ? " · " + info.loc_label : ""}`;
    $("#evOpen").href = fileUrl(info.doc_id, info.loc);
    $("#evQuote").innerHTML = highlightText(info.text, query);
    if (!info.has_page) { $("#evPage").innerHTML = ""; return; }
    const img = new Image();
    img.alt = info.loc_label;
    img.onload = () => { $("#evPage").innerHTML = ""; $("#evPage").appendChild(img); };
    img.onerror = () => { $("#evPage").innerHTML = ""; };
    img.src = `/api/evidence.png?session=${encodeURIComponent(state.sid)}&chunk=${encodeURIComponent(chunkId)}&q=${encodeURIComponent(query)}`;
  } catch (e) {
    $("#evPage").innerHTML = "";
    $("#evQuote").textContent = `${L("error")}: ${e.message}`;
  }
}

function closeEvidence() {
  $("#evidence").classList.remove("open");
  $("#scrim").classList.remove("show");
}

function addTools(body, getText) {
  const tools = document.createElement("div");
  tools.className = "msg-tools";
  const copy = document.createElement("button");
  copy.type = "button";
  copy.textContent = "⧉ " + L("copy");
  copy.onclick = async () => {
    try { await navigator.clipboard.writeText(getText()); toast(L("copied")); } catch (_) {}
  };
  tools.appendChild(copy);
  body.appendChild(tools);
}

async function ask(question) {
  question = question.trim();
  if (!question || state.busy) return;
  state.busy = true;
  $("#sendBtn").disabled = true;
  hideWelcome();
  $("#suggestions").innerHTML = "";
  addUserMessage(question);
  const { body } = addBotMessage();
  const bubble = body.querySelector(".bubble");
  bubble.innerHTML = `<div class="typing"><span></span><span></span><span></span></div>`;
  scrollDown();

  let text = "", sources = [], cited = [], frame = 0;
  const paint = () => { frame = 0; bubble.innerHTML = md(text); scrollDown(); };

  try {
    const res = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-Session-Id": state.sid },
      body: JSON.stringify({ question, doc_ids: state.selected.size ? [...state.selected] : null }),
    });
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
        if (ev.type === "sources") sources = ev.sources;
        else if (ev.type === "delta") { text += ev.text; if (!frame) frame = requestAnimationFrame(paint); }
        else if (ev.type === "done") cited = ev.cited || [];
        else if (ev.type === "error") toast(`${L("error")}: ${ev.message}`, true);
      }
    }
    if (frame) cancelAnimationFrame(frame);
    paint();
    renderSources(body, sources, cited, question + " " + text.slice(0, 300));
    addTools(body, () => text);
  } catch (e) {
    bubble.textContent = `${L("error")}: ${e.message}`;
  } finally {
    state.busy = false;
    $("#sendBtn").disabled = false;
    scrollDown();
  }
}

/* ================= режимы ================= */
function setView(view) {
  state.view = view;
  $("#viewChat").hidden = view !== "chat";
  $("#viewMap").hidden = view !== "map";
  $("#viewQuiz").hidden = view !== "quiz";
  document.querySelectorAll("#tabs button").forEach((b) => b.classList.toggle("active", b.dataset.view === view));
  $("#sidebar").classList.remove("open");
  if (view === "map") renderMap();
  if (view === "quiz") renderQuiz();
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

const emptyState = () => `<div class="empty-state"><div class="big">📂</div>${L("need_doc")}</div>`;
const loadingState = (text) => `<div class="loading"><span class="spinner"></span>${text}</div>`;
const locLink = (item) => (item.chunk_id
  ? ` <button class="loc-link" data-chunk="${esc(item.chunk_id)}" data-q="${esc(item.quote || "")}">📍 ${esc(item.loc_label || L("evidence"))}</button>`
  : "");

/* ---------- карта документа ---------- */
async function renderMap() {
  renderPicker("#mapPicker", "mapDoc", renderMap);
  const body = $("#mapBody");
  const doc = currentDoc("mapDoc");
  if (!doc) { body.innerHTML = emptyState(); return; }
  const key = `${doc.id}:${state.lang}`;
  if (!state.mapCache[key]) {
    body.innerHTML = loadingState(L("analyzing"));
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
      <section class="panel"><h4>📅 ${L("timeline")}<span class="cnt">${m.timeline.length}</span></h4>
        ${m.timeline.length ? `<ul class="timeline">${m.timeline.map((t) => `<li><div class="date">${esc(t.date || "")}</div><div class="ev">${esc(t.event || "")}${locLink(t)}</div></li>`).join("")}</ul>` : none}
      </section>
      <section class="panel"><h4>🔢 ${L("numbers")}<span class="cnt">${m.numbers.length}</span></h4>
        ${m.numbers.length ? `<div class="tiles">${m.numbers.map((n) => `<div class="tile"><div class="v">${esc(n.value || "")}</div><div class="l">${esc(n.label || "")}</div><div>${locLink(n)}</div></div>`).join("")}</div>` : none}
      </section>
      <section class="panel wide"><h4>✅ ${L("requirements")}<span class="cnt" id="reqCount">${reqDone}/${m.requirements.length} ${L("done_of")}</span></h4>
        ${m.requirements.length ? `<div class="progress"><div id="reqBar" style="width:${m.requirements.length ? (reqDone / m.requirements.length) * 100 : 0}%"></div></div>
        <ul class="checklist">${m.requirements.map((r, i) => `<li class="${done.includes(i) ? "done" : ""}"><input type="checkbox" data-i="${i}" ${done.includes(i) ? "checked" : ""}><span class="txt">${esc(r.text || "")}</span>${locLink(r)}</li>`).join("")}</ul>` : none}
      </section>
      ${m.terms.length ? `<section class="panel wide"><h4>📖 ${L("terms")}<span class="cnt">${m.terms.length}</span></h4>
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

/* ---------- проверка знаний ---------- */
function renderQuiz() {
  renderPicker("#quizPicker", "quizDoc", () => { state.quiz = null; renderQuiz(); });
  const body = $("#quizBody");
  const doc = currentDoc("quizDoc");
  if (!doc) { body.innerHTML = emptyState(); return; }
  const qz = state.quiz && state.quiz.docId === doc.id ? state.quiz : null;
  if (!qz) return paintQuizStart(doc);
  if (qz.loading) { body.innerHTML = loadingState(L("generating")); return; }
  if (qz.i >= qz.questions.length) return paintQuizResult(doc, qz);
  paintQuestion(qz);
}

function paintQuizStart(doc) {
  $("#quizBody").innerHTML = `
    <div class="quiz-start">
      <div class="big">🎓</div>
      <h3>${esc(doc.name)}</h3>
      <div class="muted">${L("quiz_intro")}</div>
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
    $("#qExplain").innerHTML = `<div class="explain"><b>${ok ? "✅ " + L("correct") : "❌ " + L("wrong")}</b>${q.explanation ? `<span>${esc(q.explanation)}</span>` : ""}${locLink(q)}</div>`;
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
        <button class="btn ghost" type="button" id="qRetry">${L("retry")}</button>
        <button class="btn" type="button" id="qNew">${L("new_quiz")}</button>
      </div>
    </div>`;
  $("#qRetry").onclick = () => { qz.i = 0; qz.answers = []; renderQuiz(); };
  $("#qNew").onclick = () => startQuiz(doc);
}

/* ================= status ================= */
function renderStatus() {
  const s = state.status;
  if (!s) return;
  const ocrOk = s.ocr && s.ocr !== "none";
  $("#status").innerHTML = `
    <div><span class="dot ${s.llm_enabled ? "ok" : "warn"}"></span>${s.llm_enabled ? `${L("llm_on")}: ${esc(s.llm_model || "")}` : L("llm_off")}</div>
    <div><span class="dot ${ocrOk ? "ok" : ""}"></span>${ocrOk ? `${L("ocr_on")}: ${esc(s.ocr)}` : L("ocr_off")}</div>
    ${s.telegram ? `<div><span class="dot ok"></span>${L("tg")}</div>` : ""}`;
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

  $("#langSwitch").onclick = (e) => {
    const lang = e.target.dataset.lang;
    if (!lang) return;
    state.lang = lang;
    try { localStorage.setItem("docmind_lang", lang); } catch (_) {}
    applyI18n();
  };

  const fileInput = $("#fileInput");
  fileInput.onchange = () => uploadFiles(fileInput.files);
  $("#attachBtn").onclick = () => fileInput.click();

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

  $("#clearChat").onclick = async () => {
    await api("/api/clear", { method: "POST" });
    $("#messages").innerHTML = "";
    $("#suggestions").innerHTML = "";
    $("#welcome").style.display = "";
    toast(L("cleared"));
  };

  $("#tabs").onclick = (e) => { const b = e.target.closest("button"); if (b) setView(b.dataset.view); };
  $("#evClose").onclick = closeEvidence;
  $("#scrim").onclick = closeEvidence;
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeEvidence(); });
  // ссылки «📍 стр. N» в карте документа и в тесте
  document.addEventListener("click", (e) => {
    const link = e.target.closest(".loc-link");
    if (link) openEvidence(link.dataset.chunk, link.dataset.q);
  });

  $("#openSidebar").onclick = () => $("#sidebar").classList.add("open");
  $("#closeSidebar").onclick = () => $("#sidebar").classList.remove("open");

  api("/api/status").then((s) => { state.status = s; renderStatus(); }).catch(() => {});
  loadDocs().catch((e) => toast(e.message, true));
}

init();
