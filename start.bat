@echo off
title MindCare 360 - Running
echo ============================================
echo   MindCare 360 v3.0 - Starting Server
echo ============================================
echo.

:: Check venv exists
if not exist env\Scripts\activate.bat (
    echo ERROR: Virtual environment not found. Run setup.bat first.
    pause
    exit /b 1
)

:: Check .env
if not exist .env (
    echo ERROR: .env file not found. Run setup.bat first.
    pause
    exit /b 1
)

:: Check if key is still placeholder
findstr /c:"paste_your_groq_key_here" .env >nul 2>&1
if not errorlevel 1 (
    echo ERROR: You haven't set your GROQ_API_KEY in the .env file yet!
    echo Open .env in Notepad and replace: paste_your_groq_key_here
    echo with your real key from https://console.groq.com
    echo.
    pause
    exit /b 1
)

call env\Scripts\activate.bat

echo Starting server at http://localhost:8000
echo Press Ctrl+C to stop.
echo.

:: Open browser after 2 seconds
start "" timeout /t 2 >nul && start http://localhost:8000

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
