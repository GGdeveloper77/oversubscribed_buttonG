@echo off
echo ========================================
echo 🚀 FREE CRYPTO SCANNER - ONE CLICK!
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python first.
    pause
    exit /b 1
)

echo ✅ Python found!
echo.

REM Install requirements if needed
echo 📦 Installing/updating dependencies...
pip install -r requirements.txt >nul 2>&1

echo.
echo 🔍 Starting crypto projects scanner...
echo ⏱️  This may take 1-2 minutes...
echo.

REM Run the scanner
python run_scanner_local.py

echo.
echo ✨ Scanner finished! Check the output above.
echo 📊 Results should be in your Google Sheets.
echo.
pause 