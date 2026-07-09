@echo off
title MindCare 360 - Setup
echo ============================================
echo   MindCare 360 - First Time Setup
echo ============================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Install Python 3.10+ from python.org
    pause
    exit /b 1
)

:: Create virtual environment
echo [1/3] Creating virtual environment...
python -m venv env
if errorlevel 1 (
    echo ERROR: Could not create venv
    pause
    exit /b 1
)

:: Activate and install
echo [2/3] Installing packages (this takes a minute)...
call env\Scripts\activate.bat
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: pip install failed
    pause
    exit /b 1
)

:: Create .env if missing
if not exist .env (
    echo [3/3] Creating .env file...
    echo GROQ_API_KEY=paste_your_groq_key_here > .env
    echo.
    echo *** IMPORTANT: Open .env and replace the placeholder with your real Groq API key ***
    echo *** Get your free key at: https://console.groq.com ***
    echo.
) else (
    echo [3/3] .env already exists, skipping.
)

echo.
echo ============================================
echo   Setup complete! Run start.bat to launch.
echo ============================================
pause
