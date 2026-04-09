@echo off
REM ============================================================
REM  Vacation Agent - Test Script (Windows)
REM  Tests the Python agent and sends a test prompt
REM ============================================================

setlocal
set "AGENT_DIR=%~dp0"
set "PYTHON_PATH=C:\Program Files\Python314\python.exe"

echo.
echo ========================================
echo  Vacation Agent - Test Suite
echo ========================================
echo.

REM Check Python
if not exist "%PYTHON_PATH%" (
    echo Trying alternate Python path...
    set "PYTHON_PATH=python"
)

echo [1/4] Checking Python...
%PYTHON_PATH% --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo [2/4] Checking dependencies...
%PYTHON_PATH% -c "import pydantic; import dotenv; print('  All dependencies OK')"
if errorlevel 1 (
    echo Installing dependencies...
    %PYTHON_PATH% -m pip install -r "%AGENT_DIR%requirements.txt" --quiet --user
)

echo [3/4] Testing Vacation Agent core...
echo.
cd /d "%AGENT_DIR%"
%PYTHON_PATH% tests\run_tests.py
if errorlevel 1 (
    echo.
    echo ERROR: Core tests failed!
    pause
    exit /b 1
)

echo [4/4] Testing with live prompt...
echo.
echo --- Sending test prompt ---
echo.
%PYTHON_PATH% tests\send_test_prompt.py

echo.
echo ========================================
echo  Test Complete!
echo ========================================
echo.

pause
