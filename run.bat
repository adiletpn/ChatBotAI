@echo off
REM Запуск DocMind AI на Windows. Двойной щелчок по файлу.
chcp 65001 >nul
cd /d "%~dp0"

if not exist .venv (
  echo Creating virtual environment...
  python -m venv .venv
  .venv\Scripts\python -m pip install --upgrade pip
  .venv\Scripts\pip install -r requirements.txt
)

if not exist .env (
  copy .env.example .env >nul
  echo Created .env - put your LLM_API_KEY and LLM_BASE_URL there.
)

echo Open in browser: http://localhost:8000
.venv\Scripts\python -m app.main
pause
