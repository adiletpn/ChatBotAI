"""Сквозная проверка без LLM: загрузка демо-документов, поиск, офлайн-ответы, API.

Запуск:  .venv/bin/python tests/smoke_test.py
"""
import asyncio
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ["DATA_DIR"] = tempfile.mkdtemp(prefix="docmind_test_")
os.environ["LLM_API_KEY"] = ""  # проверяем офлайн-режим
os.environ["TELEGRAM_BOT_TOKEN"] = ""

from fastapi.testclient import TestClient  # noqa: E402

from app import rag  # noqa: E402
from app.config import settings  # noqa: E402
from app.lang import detect_lang  # noqa: E402
from app.main import app  # noqa: E402
from app.ocr import ocr_engine  # noqa: E402
from app.store import store  # noqa: E402

SAMPLES = ROOT / "samples"
failures = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global failures
    print(("  ✅ " if ok else "  ❌ ") + name + (f" — {detail}" if detail else ""))
    failures += 0 if ok else 1


async def ask(question: str, owner: str) -> dict:
    return await rag.answer(question, owner, owner + ":" + question)


async def main() -> None:
    settings.llm_api_key = ""
    print("Язык:")
    check("kk", detect_lang("Финал қашан өтеді?") == "kk")
    check("ru", detect_lang("Когда пройдёт финал?") == "ru")
    check("en", detect_lang("When is the final?") == "en")

    print("Загрузка документов:")
    owner = "test"
    pdf = rag.ingest(owner, "Ereje.pdf", (SAMPLES / "Innovation_AI_Hackathon_2026_Ereje.pdf").read_bytes())
    check("PDF", pdf["pages"] == 2 and pdf["chunks"] > 5 and pdf["lang"] == "kk", str(pdf))
    docx = rag.ingest(owner, "Instr.docx", (SAMPLES / "Instrukciya_po_ohrane_truda.docx").read_bytes())
    check("DOCX + таблица", docx["chunks"] >= 2 and docx["lang"] == "ru", str(docx))
    txt = rag.ingest(owner, "note.txt", "Wi-Fi пароль в офисе: Talap2026. Обед с 13:00 до 14:00.".encode("cp1251"))
    check("TXT (cp1251)", txt["chars"] > 20)

    print(f"OCR ({ocr_engine()}):")
    if ocr_engine() != "none":
        scan = rag.ingest(owner, "scan.pdf", (SAMPLES / "Scan_AIChatBots_talaptary.pdf").read_bytes())
        check("скан распознан", scan["ocr_pages"] == 1 and scan["chars"] > 100, str(scan))
        scan_text = " ".join(c["text"] for c in store.doc_chunks({scan["id"]}))
        check("текст скана", "балл" in scan_text.lower(), scan_text[:120])
    else:
        print("  ⚠️  OCR недоступен — пропуск")

    print("Поиск и офлайн-ответы:")
    settings.full_context_chars = 0  # принудительно режим поиска (BM25)
    cases = [
        ("Финалдық кезең қашан өтеді?", "14 қараша"),
        ("Команда құрамында неше адам болуы мүмкін?", "үш адамнан"),
        ("Как часто проводится повторный инструктаж?", "6 месяцев"),
        ("Срок носки защитной каски?", "24 месяца"),
        ("Какой пароль от Wi-Fi?", "Talap2026"),
    ]
    for question, expected in cases:
        result = await ask(question, owner)
        ok = expected.lower() in result["text"].lower() and bool(result["sources"])
        loc = result["sources"][0]["loc_label"] if result["sources"] else "-"
        check(question, ok, f"источник: {result['sources'][0]['doc_name'] if result['sources'] else '-'} {loc}")

    result = await ask("Финал қашан?", "nobody")
    check("нет документов → подсказка", "құжат" in result["text"].lower())

    print("REST API:")
    client = TestClient(app)
    headers = {"X-Session-Id": "smoketest123"}
    r = client.get("/api/status")
    check("/api/status", r.status_code == 200 and r.json()["llm_enabled"] is False)
    with open(SAMPLES / "Instrukciya_po_ohrane_truda.docx", "rb") as f:
        r = client.post("/api/documents", headers=headers, files={"files": ("instr.docx", f)})
    check("загрузка через API", r.status_code == 200 and "id" in r.json()[0], r.text[:200])
    doc_id = r.json()[0]["id"]
    r = client.post("/api/ask", headers=headers, json={"question": "Какой номер вызова пожарной службы?"})
    check("стриминг /api/ask", r.status_code == 200 and "101" in r.text, r.text[:150])
    r = client.get(f"/api/documents/{doc_id}/summary?lang=ru", headers=headers)
    check("резюме", r.status_code == 200 and r.json()["summary"])
    r = client.get(f"/api/documents/{doc_id}/insights?lang=ru", headers=headers)
    check("карта документа", r.status_code == 200 and len(r.json()["numbers"]) >= 3 and r.json()["requirements"])
    r = client.get(f"/api/documents/{doc_id}/quiz?lang=ru&n=3", headers=headers)
    quiz = r.json().get("questions", [])
    check("тест по документу", r.status_code == 200 and len(quiz) >= 2
          and all(q["options"][q["answer"]] in q["quote"] for q in quiz), str(quiz[:1])[:150])
    with open(SAMPLES / "Innovation_AI_Hackathon_2026_Ereje.pdf", "rb") as f:
        pdf_id = client.post("/api/documents", headers=headers, files={"files": ("ereje.pdf", f)}).json()[0]["id"]
    chunk_id = f"{pdf_id}:0"
    r = client.get(f"/api/chunk?chunk={chunk_id}", headers=headers)
    check("фрагмент-доказательство", r.status_code == 200 and r.json()["has_page"])
    r = client.get(f"/api/evidence.png?session=smoketest123&chunk={chunk_id}&q=Жамбыл облысы")
    check("страница с подсветкой", r.status_code == 200 and r.content[:4] == b"\x89PNG")
    r = client.get(f"/api/evidence.png?session=other_session&chunk={chunk_id}")
    check("чужая страница недоступна", r.status_code == 404)
    client.delete(f"/api/documents/{pdf_id}", headers=headers)
    r = client.get(f"/api/documents/{doc_id}/file?session=smoketest123")
    check("скачивание оригинала", r.status_code == 200 and len(r.content) > 1000)
    r = client.get(f"/api/documents/{doc_id}/file?session=other_session")
    check("чужой документ недоступен", r.status_code == 404)
    r = client.post("/api/documents", headers=headers, files={"files": ("virus.exe", b"MZ")})
    check("неподдерживаемый формат", "error" in r.json()[0])
    r = client.delete(f"/api/documents/{doc_id}", headers=headers)
    check("удаление", r.status_code == 200 and client.get("/api/documents", headers=headers).json() == [])

    print("\nИТОГ:", "все проверки пройдены ✅" if not failures else f"ошибок: {failures} ❌")
    sys.exit(1 if failures else 0)


asyncio.run(main())
