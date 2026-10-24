#!/usr/bin/env bash
# Запуск DocMind AI на macOS / Linux.  Использование:  ./run.sh
set -e
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  echo "▶ Создаю виртуальное окружение..."
  python3 -m venv .venv
  .venv/bin/pip install --upgrade pip
  .venv/bin/pip install -r requirements.txt
fi

if [ ! -f .env ]; then
  cp .env.example .env
  echo "▶ Создан файл .env — впишите в него ключ API (LLM_API_KEY) и адрес (LLM_BASE_URL)."
fi

if ! command -v tesseract >/dev/null 2>&1; then
  echo "⚠ Tesseract не найден — сканы распознаваться не будут. Установка: brew install tesseract"
fi

echo "▶ Открывайте в браузере: http://localhost:${PORT:-8000}"
exec .venv/bin/python -m app.main
