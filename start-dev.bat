@echo off
echo ============================================
echo  SNSU Tracker - Development Server Startup
echo ============================================
echo.

REM Check for required tools
where uv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: uv is not installed. Install from https://docs.astral.sh/uv/
    pause
    exit /b 1
)

where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Node.js is not installed. Install from https://nodejs.org/
    pause
    exit /b 1
)

REM Install/sync backend dependencies
echo Installing backend dependencies...
cd backend
uv sync
if %ERRORLEVEL% neq 0 (
    echo ERROR: Backend dependency install failed.
    pause
    exit /b 1
)
cd ..

REM Install frontend dependencies
echo Installing frontend dependencies...
cd frontend
if not exist node_modules (
    echo node_modules not found, running npm install...
    call npm install
) else (
    echo node_modules found, verifying...
    call npm install
)
if %ERRORLEVEL% neq 0 (
    echo ERROR: Frontend dependency install failed.
    pause
    exit /b 1
)
cd ..

echo.
echo Starting servers...
start "Backend" cmd /k "cd backend && uv run uvicorn main:app --reload"
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:5173/
echo Press any key to close...
pause >nul
