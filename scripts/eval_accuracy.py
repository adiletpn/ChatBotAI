"""Прогон точности Mind AI: 45 вопросов с заранее известными ответами по демо-документам.

Что проверяется:
  * ответ верный — в нём есть ожидаемые факты (число, дата, название);
  * источник верный — бот сослался на правильный документ и страницу;
  * ловушки — на вопросы, ответа на которые в документах нет, бот честно говорит «не нашёл», а не выдумывает.

Вопросы на трёх языках, в том числе «крест-накрест» (вопрос на русском — документ на казахском),
вопросы по смыслу без общих слов с текстом и вопросы по таблице.

Запуск:  .venv/bin/python scripts/eval_accuracy.py            (нужен LLM_API_KEY в .env)
"""
import asyncio
import os
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DATA_DIR", tempfile.mkdtemp(prefix="mind_eval_"))
os.environ.setdefault("MODELS_DIR", str(Path.home() / ".cache" / "mind-ai-models"))

from app import rag  # noqa: E402
from app.config import settings  # noqa: E402
from app.semantic import semantic  # noqa: E402
from app.store import store  # noqa: E402

EREJE, INSTR = "Ereje.pdf", "Instr.docx"
# (вопрос, группы ожидаемых фрагментов — из каждой группы должен найтись хотя бы один, документ, страницы)
CASES = [
    ("Финал қашан өтеді?", [["14 қараша", "14 ноябр"]], EREJE, {1}, "kk → kk"),
    ("Когда пройдёт финал чемпионата?", [["14 ноябр", "14 қараша"]], EREJE, {1}, "ru → kk"),
    ("When is the final?", [["14", "november"], ["november", "ноябр", "қараша"]], EREJE, {1}, "en → kk"),
    ("До какого числа нужно зарегистрироваться?", [["25 октябр", "25 қазан"]], EREJE, {1}, "ru → kk"),
    ("Сколько человек может быть в команде?", [["три", "трех", "трое", "3", "үш"]], EREJE, {1}, "ru → kk"),
    ("Жетекші команда қатысушыларының санына кіре ме?", [["кірмейді", "жоқ", "кірмей"]], EREJE, {1}, "kk → kk"),
    ("Какой возраст участников?", [["16"], ["20"]], EREJE, {1}, "ru → kk"),
    ("Кто организаторы чемпионата?", [["жамбыл"], ["talap"]], EREJE, {1}, "ru → kk"),
    ("Какие рабочие языки чемпионата?", [["казах", "қазақ"], ["русск", "орыс"], ["англ", "ағылшын"]], EREJE, {1}, "ru → kk"),
    ("Куда отправить проект по почте?", [["it@jihc.edu.kz"]], EREJE, {1, 2}, "ru → kk"),
    ("Сколько минут даётся на презентацию проекта в финале?", [["7"]], EREJE, {2}, "ru → kk"),
    ("Сколько всего времени даётся команде на защите?", [["12"]], EREJE, {2}, "ru → kk"),
    ("Сколько направлений у чемпионата?", [["4", "четыр", "төрт"]], EREJE, {2}, "ru → kk"),
    ("Сколько баллов дают за точность ответов в AIChatBots?", [["30"]], EREJE, {2}, "ru → kk"),
    ("AIChatBots бағыты бойынша идеяның өзектілігіне қанша балл беріледі?", [["40"]], EREJE, {2}, "kk → kk"),
    ("Какой длины должен быть видеоролик?", [["5"], ["7"]], EREJE, {2}, "ru → kk"),
    ("Через какие платформы может быть доступен чат-бот?", [["telegram"], ["whatsapp"]], EREJE, {2}, "ru → kk"),
    ("Сколько минимум членов жюри?", [["три", "трех", "трое", "3", "үш"]], EREJE, {2}, "ru → kk"),
    ("Как считается итоговый балл команды?", [["средн", "орташа"]], EREJE, {2}, "ru → kk"),
    ("How many prize places are there in each track?", [["3", "three", "i, ii", "iii"]], EREJE, {2}, "en → kk"),
    ("Какой телефон для связи с организаторами?", [["931 42 76", "9314276"]], EREJE, {2}, "ru → kk"),
    ("Можно ли нескольким командам от одного колледжа участвовать?", [["можно", "разреш", "да", "рұқсат"]], EREJE, {1}, "ru → kk"),
    ("Что даёт чат-боту дополнительные баллы?", [["источник", "дереккөз"], ["язык", "тіл"], ["скан"]], EREJE, {2}, "по смыслу"),
    ("Как часто проводится повторный инструктаж?", [["6 месяц", "шесть месяц", "полгода"]], INSTR, None, "ru → ru"),
    ("Срок носки защитной каски?", [["24"]], INSTR, None, "таблица"),
    ("Каска мерзімі қанша?", [["24"]], INSTR, None, "kk → ru, таблица"),
    ("How long can a safety helmet be worn?", [["24"]], INSTR, None, "en → ru, таблица"),
    ("Когда обязательны противошумные наушники?", [["80"]], INSTR, None, "таблица"),
    ("С какого возраста допускают к самостоятельной работе?", [["18"]], INSTR, None, "ru → ru"),
    ("Сколько смен длится стажировка?", [["5"]], INSTR, None, "ru → ru"),
    ("По какому номеру вызвать пожарных?", [["101"]], INSTR, None, "ru → ru"),
    ("Өрт кезінде қай нөмірге қоңырау шалу керек?", [["101"]], INSTR, None, "kk → ru"),
    ("Что делать, если человек получил травму?", [["перв", "алғашқы", "first aid"], ["103"]], INSTR, None, "по смыслу"),
    ("С какой высоты нужна страховочная привязь?", [["1,8", "1.8"]], INSTR, None, "ru → ru"),
    ("Кто следит за соблюдением инструкции?", [["инженер", "engineer"]], INSTR, None, "по смыслу"),
    ("Когда проводится внеплановый инструктаж?", [["технолог"], ["несчастн"], ["60"]], INSTR, None, "ru → ru"),
    ("Что нужно проверить перед началом работы?", [["заземл"], ["стоп"]], INSTR, None, "ru → ru"),
    ("Как часто выдают защитную обувь?", [["12"]], INSTR, None, "таблица"),
    ("Какой единый номер экстренных служб?", [["112"]], INSTR, None, "ru → ru"),
]
TRAPS = [
    "Какая зарплата у работника цеха?",
    "Сколько стоит участие в хакатоне?",
    "Кто победил в чемпионате в прошлом году?",
    "Финалда қатысушыларға тамақ беріле ме?",
    "What is the capital of France?",
    "Сколько дней отпуска положено работнику?",
]
NOT_FOUND = ["не нашлось", "не найден", "нет информации", "не содерж", "не указ", "отсутству", "не упомина",
             "таба алмадым", "жоқ", "көрсетілмеген", "айтылмаған", "could not find", "not found", "does not",
             "no information", "not mentioned", "not specified", "don't", "do not"]


def norm(text: str) -> str:
    return text.lower().replace("ё", "е").replace(" ", " ").replace("**", "")


async def main() -> None:
    if not settings.llm_enabled:
        sys.exit("Нужен LLM_API_KEY в .env — прогон проверяет ответы модели")
    semantic.start(lambda: list(store.chunks))
    for _ in range(600):
        if semantic.ready or semantic.error:
            break
        time.sleep(0.5)
    owner = "eval"
    rag.ingest(owner, EREJE, (ROOT / "samples/Innovation_AI_Hackathon_2026_Ereje.pdf").read_bytes())
    rag.ingest(owner, INSTR, (ROOT / "samples/Instrukciya_po_ohrane_truda.docx").read_bytes())
    settings.full_context_chars = 0  # честный режим поиска: модель видит только найденные фрагменты

    ok_answer = ok_source = 0
    times, failed = [], []
    print(f"Модель: {settings.llm_model} · поиск по смыслу: {'да' if semantic.ready else 'нет'}\n")
    for i, (question, groups, doc, pages, kind) in enumerate(CASES, 1):
        t = time.time()
        result = await rag.answer(question, owner, f"{owner}:{i}")
        times.append(time.time() - t)
        text = norm(result["text"])
        answer_ok = all(any(norm(alt) in text for alt in group) for group in groups)
        source_ok = any(s["doc_name"] == doc and (pages is None or s["loc"].get("value") in pages)
                        for s in result["sources"])
        ok_answer += answer_ok
        ok_source += source_ok
        mark = "✅" if answer_ok and source_ok else ("⚠️" if answer_ok else "❌")
        print(f"{mark} {i:2}. [{kind}] {question}")
        if not (answer_ok and source_ok):
            failed.append(i)
            print(f"      ответ: {result['text'][:200].replace(chr(10), ' ')}")
            print(f"      источники: {[(s['doc_name'], s['loc_label']) for s in result['sources']]}")

    honest = 0
    print("\nЛовушки (ответа в документах нет):")
    for j, question in enumerate(TRAPS, 1):
        t = time.time()
        result = await rag.answer(question, owner, f"{owner}:trap{j}")
        times.append(time.time() - t)
        is_honest = any(p in norm(result["text"]) for p in NOT_FOUND)
        honest += is_honest
        print(f"{'✅' if is_honest else '❌'} {question}")
        if not is_honest:
            print(f"      ответ: {result['text'][:200].replace(chr(10), ' ')}")

    n = len(CASES)
    print("\n" + "=" * 60)
    print(f"Правильный ответ:         {ok_answer}/{n} = {ok_answer / n:.0%}")
    print(f"Правильный источник:      {ok_source}/{n} = {ok_source / n:.0%}")
    print(f"Честно «не нашёл» на ловушках: {honest}/{len(TRAPS)} = {honest / len(TRAPS):.0%}")
    print(f"Среднее время ответа:     {sum(times) / len(times):.1f} с")
    if failed:
        print(f"Не прошли: {failed}")


asyncio.run(main())
