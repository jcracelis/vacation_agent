@echo off
REM ============================================================
REM  Vacation Agent - One-Click Setup
REM  Double-click this file to run the full setup
REM ============================================================

setlocal

set "PYTHON_PATH=C:\Program Files\Python314\python.exe"
set "AGENT_DIR=%~dp0"
set "VSCODE_DIR=%AGENT_DIR%vscode-extension"

echo.
echo ========================================
echo  Vacation Agent Setup
echo ========================================
echo.

REM Step 1: Python deps
echo [1/3] Installing Python dependencies...
if exist "%PYTHON_PATH%" (
    "%PYTHON_PATH%" -m pip install -r "%AGENT_DIR%requirements.txt" --quiet --user >nul 2>&1
    echo  Done.
) else (
    echo  Python not found at %PYTHON_PATH%, trying 'python'...
    python -m pip install -r "%AGENT_DIR%requirements.txt" --quiet --user >nul 2>&1
    echo  Done.
)

REM Step 2: Compile extension
echo [2/3] Compiling VS Code extension...
cd /d "%VSCODE_DIR%"
call npm install >nul 2>&1
call npm run compile >nul 2>&1
echo  Done.

REM Step 3: Check Ollama and open VS Code
echo [3/3] Checking Ollama...
where ollama >nul 2>&1
if %errorlevel% equ 0 (
    echo  Ollama found. Starting server...
    start /B ollama serve
    timeout /t 2 /nobreak >nul
    echo  Opening VS Code...
    cd /d "%VSCODE_DIR%"
    code .
) else (
    echo.
    echo  Ollama is NOT installed.
    echo  To install: https://ollama.com/download/windows
    echo.
    echo  Opening VS Code anyway (will work without Ollama)...
    echo  For full LLM responses, install Ollama or set an API key.
    echo.
    cd /d "%VSCODE_DIR%"
    code .
)

echo.
echo ========================================
echo  Setup complete!
echo.
echo  In VS Code:
echo   1. Press F5
echo   2. Click the vacation agent icon
echo   3. Start chatting!
echo ========================================
echo.

timeout /t 5
