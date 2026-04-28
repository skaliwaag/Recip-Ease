@echo off
setlocal enabledelayedexpansion

echo.
echo === Recip-Ease Setup ===
echo.

:: 1. Virtual environment
if not exist "venv\" (
    echo [1/5] Creating virtual environment...
    python -m venv venv
) else (
    echo [1/5] Virtual environment found.
)

:: 2. Dependencies
echo [2/5] Installing dependencies...
venv\Scripts\pip install -r requirements.txt -q

:: 3. .env
echo [3/5] Checking environment config...
if not exist ".env" (
    copy .env.example .env > nul
    echo.
    echo   .env created from .env.example.
    echo   Opening .env in Notepad — set your MONGO_URI, save, and close.
    notepad .env
    echo   .env configured.
) else (
    echo   .env already exists.
)

:: 4. Seed database
echo [4/5] Seeding database...
venv\Scripts\python seed_db.py

:: 5. Create indexes
echo [5/5] Creating indexes...
venv\Scripts\python create_indexes.py

echo.
echo === Setup complete. Starting app ===
echo     Open http://127.0.0.1:5000 in your browser.
echo.
venv\Scripts\python run.py
