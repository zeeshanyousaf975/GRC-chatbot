@echo off
echo Setting up development environment for Chat Agent...
echo.

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.9+ and try again.
    exit /b 1
)

REM Check if Node.js is installed
node --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Node.js is not installed or not in PATH.
    echo Please install Node.js 16+ and try again.
    exit /b 1
)

echo Setting up backend...
cd backend

REM Check if .env exists, if not copy from .env-example
if not exist .env (
    if exist .env-example (
        echo Creating .env from .env-example...
        copy .env-example .env
        echo Please edit backend\.env and set your GROQ_API_KEY.
    ) else (
        echo Warning: .env-example not found. Please create a .env file manually.
    )
)

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment and install dependencies
echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt

echo.
echo Backend setup complete.
echo.

REM Return to root directory
cd ..

echo Setting up frontend...
cd frontend

REM Run the dev setup script
echo Running frontend setup script...
node dev-setup.js

REM Install dependencies
echo Installing frontend dependencies...
npm install

echo.
echo Frontend setup complete.
echo.

REM Return to root directory
cd ..

echo.
echo Development environment setup complete!
echo.
echo To start the backend:
echo   cd backend
echo   venv\Scripts\activate
echo   python run_dev.py
echo.
echo To start the frontend:
echo   cd frontend
echo   npm start
echo.
echo Remember to set your GROQ_API_KEY in backend\.env before running! 