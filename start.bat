@echo off
REM Summify Startup Script for Windows

echo 🚀 Starting Summify...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if OPENAI_API_KEY is set
if "%OPENAI_API_KEY%"=="" (
    echo ⚠️  OPENAI_API_KEY is not set!
    echo Please set it before running:
    echo.
    echo set OPENAI_API_KEY=your-api-key-here
    echo.
    
    REM Try to load from .env file
    if exist ".env" (
        echo Loading from .env file...
        for /f "tokens=*" %%i in (.env) do (
            if not "%%i"=="" if not "%%i:~0,1%"=="#" (
                set %%i
            )
        )
    ) else (
        echo ❌ .env file not found. Create one using .env.example
        pause
        exit /b 1
    )
)

REM Install/upgrade dependencies if needed
echo 📦 Checking dependencies...
pip install -q -r requirements.txt

REM Start the server
echo.
echo ✅ Starting FastAPI server...
echo 🌐 Application will be available at: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
