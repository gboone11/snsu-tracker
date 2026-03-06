@echo off
echo Starting development servers...

start "Backend" cmd /k "cd backend && uv run uvicorn main:app --reload"
start "Frontend" cmd /k "cd frontend && npm run dev"

echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:5173/
echo Press any key to close...
pause >nul