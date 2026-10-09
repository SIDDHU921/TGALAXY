@echo off
echo =====================================================================
echo  Starting SentinX: Smart Spam Detection & Security Layer
echo =====================================================================
echo.

echo [1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "SentinX Backend (FastAPI)" cmd /k "cd /d %~dp0backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo [2/2] Starting React Frontend on http://localhost:5173 ...
start "SentinX Frontend (Vite)" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo Both servers are launching!
echo Backend API Docs: http://127.0.0.1:8000/docs
echo Frontend Dashboard: http://localhost:5173
echo.
pause
