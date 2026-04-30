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
:: Upgrade pip first so teammates don't see the "new version available" warning mid-install
venv\Scripts\pip install --upgrade pip -q
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
echo.
echo   Opening http://127.0.0.1:5000 in 5 seconds. Press ESC to cancel.
echo.

:: Poll for ESC once per ms during each 1-second tick; exit 1 on cancel so the
:: next line can gate the browser launch on errorlevel
powershell -NoProfile -Command "$c=$false;for($i=5;$i-ge1;$i--){Write-Host -NoNewline \"`r  $i...  \";$sw=[Diagnostics.Stopwatch]::StartNew();while($sw.Elapsed.TotalSeconds-lt 1){if([Console]::KeyAvailable){$k=[Console]::ReadKey($true);if($k.Key-eq 'Escape'){$c=$true;break}}};if($c){break}};if($c){Write-Host \"`r  Browser launch cancelled.     \";exit 1}else{Write-Host ''}"
:: Only open the browser if PowerShell exited cleanly (errorlevel 0 = not cancelled)
if not errorlevel 1 start "" http://127.0.0.1:5000

venv\Scripts\python run.py
