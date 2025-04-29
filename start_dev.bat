@echo off
echo Starting Chat Agent development servers...
echo.

REM Check if both backend and frontend directories exist
if not exist backend\ (
    echo Backend directory not found.
    echo Please run this script from the project root directory.
    exit /b 1
)

if not exist frontend\ (
    echo Frontend directory not found.
    echo Please run this script from the project root directory.
    exit /b 1
)

REM Start backend server in a new window
echo Starting backend server...
start cmd /k "cd backend && call venv\Scripts\activate && python run_dev.py"

REM Wait a bit for backend to start
timeout /t 5 /nobreak > nul

REM Start frontend server in a new window
echo Starting frontend server...
start cmd /k "cd frontend && npm start"

echo.
echo Development servers started!
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window...
pause > nul 