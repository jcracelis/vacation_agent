@echo off
setlocal
set "PYTHON_PATH=C:\Program Files\Python314\python.exe"
set "AGENT_DIR=%~dp0"
set "VSCODE_DIR=%AGENT_DIR%vscode-extension"

echo.
echo ========================================
echo  Vacation Agent Setup
echo ========================================
echo.

echo [1/3] Installing Python dependencies...
if exist "%PYTHON_PATH%" (
    "%PYTHON_PATH%" -m pip install -r "%AGENT_DIR%requirements.txt" --quiet --user
) else (
    python -m pip install -r "%AGENT_DIR%requirements.txt" --quiet --user
)
echo  Done.

echo [2/3] Compiling VS Code extension...
cd /d "%VSCODE_DIR%"
call npm install
call npm run compile
echo  Done.

echo [3/3] Checking Ollama...
where ollama >nul 2>&1
if %errorlevel% equ 0 (
    echo  Ollama found. Starting server...
    start /B ollama serve
    timeout /t 2 /nobreak >nul
) else (
    echo  Ollama not found. Install from: https://ollama.com/download/windows
    echo  Then run: ollama pull llama3
)

echo.
echo Opening VS Code...
cd /d "%VSCODE_DIR%"
code .

echo.
echo ========================================
echo  In VS Code:
echo   1. Press F5
echo   2. Click the vacation agent icon
echo   3. Start chatting!
echo ========================================
echo.
