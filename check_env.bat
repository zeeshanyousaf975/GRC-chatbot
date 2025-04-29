@echo off
echo Checking environment for Chat Agent development...
echo.

set ERROR=0

echo Checking Python...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [FAILED] Python not found.
    echo Please install Python 3.9+ and add it to your PATH.
    set ERROR=1
) else (
    for /f "tokens=2" %%a in ('python --version 2^>^&1') do set pyver=%%a
    echo [OK] Python %pyver% detected.
)

echo Checking Node.js...
node --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [FAILED] Node.js not found.
    echo Please install Node.js 16+ and add it to your PATH.
    set ERROR=1
) else (
    for /f "tokens=1" %%a in ('node --version') do set nodever=%%a
    echo [OK] Node.js %nodever% detected.
)

echo Checking npm...
npm --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [FAILED] npm not found.
    echo Please install npm (it should come with Node.js).
    set ERROR=1
) else (
    for /f "tokens=1" %%a in ('npm --version') do set npmver=%%a
    echo [OK] npm %npmver% detected.
)

echo Checking backend setup...
if not exist backend\venv\ (
    echo [WARNING] Virtual environment not found in backend folder.
    echo Run setup_dev.bat to create it.
) else (
    echo [OK] Backend virtual environment exists.
)

if not exist backend\.env (
    echo [WARNING] .env file not found in backend folder.
    echo Please create backend\.env file with your GROQ_API_KEY.
) else (
    echo [OK] Backend .env file exists.
    
    REM Check if GROQ_API_KEY is set in .env
    findstr /C:"GROQ_API_KEY=your_groq_api_key_here" backend\.env > nul 2>&1
    if %errorlevel% equ 0 (
        echo [WARNING] GROQ_API_KEY appears to be using the default value.
        echo Please set your actual Groq API key in the backend\.env file.
    ) else (
        findstr /C:"GROQ_API_KEY=" backend\.env > nul 2>&1
        if %errorlevel% equ 0 (
            echo [OK] GROQ_API_KEY appears to be set.
        ) else (
            echo [WARNING] GROQ_API_KEY not found in .env file.
            echo Please add GROQ_API_KEY=your_key to the backend\.env file.
        )
    )
)

echo Checking frontend setup...
if not exist frontend\node_modules\ (
    echo [WARNING] Node modules not found in frontend folder.
    echo Run setup_dev.bat or 'cd frontend && npm install'.
) else (
    echo [OK] Frontend node_modules exists.
)

echo.
if %ERROR% equ 0 (
    echo Environment check complete. Your system appears to be ready for development.
) else (
    echo Environment check complete with some issues. Please fix the problems above.
)
echo.
echo Press any key to exit...
pause > nul 