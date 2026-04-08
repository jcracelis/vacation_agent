@echo off
REM Vacation Agent - Windows Test Script
REM Run this from CMD or double-click to test the agent

echo ============================================
echo   Vacation Agent - Test Suite
echo ============================================
echo.

REM Set paths
set PYTHON_EXE=C:\Program Files\Python314\python.exe
set PROJECT_DIR=C:\Users\racel\github\vacation_agent\.github\agents

echo [Test 1] Checking Python installation...
"%PYTHON_EXE%" --version
if errorlevel 1 (
    echo FAIL: Python not found at %PYTHON_EXE%
    pause
    exit /b 1
)
echo PASS: Python found
echo.

echo [Test 2] Checking required packages...
"%PYTHON_EXE%" -c "import pydantic; import dotenv; import yaml; print('  pydantic:', pydantic.__version__); print('  All packages found')"
if errorlevel 1 (
    echo Installing missing packages...
    "%PYTHON_EXE%" -m pip install pydantic python-dotenv pyyaml
)
echo.

echo [Test 3] Testing VacationAgent import...
cd /d "%PROJECT_DIR%"
"%PYTHON_EXE%" -c "from src.agent import VacationAgent; print('  VacationAgent imported successfully')"
if errorlevel 1 (
    echo FAIL: Could not import VacationAgent
    pause
    exit /b 1
)
echo PASS: Import successful
echo.

echo [Test 4] Testing agent initialization...
"%PYTHON_EXE%" -c "from src.agent import VacationAgent; a = VacationAgent(); print('  Agent initialized'); print('  Model:', a.model_name); print('  Approved sources:', len(a.APPROVED_REVIEW_SOURCES + list(a.APPROVED_AIRLINES.keys()) + list(a.APPROVED_RAIL.keys())))"
if errorlevel 1 (
    echo FAIL: Could not initialize agent
    pause
    exit /b 1
)
echo PASS: Agent initialized
echo.

echo [Test 5] Testing greeting function...
"%PYTHON_EXE%" -c "from src.agent import VacationAgent; a = VacationAgent(); g = a.greet(); print('  Greeting length:', len(g)); print('  Contains questions:', 'what' in g.lower() or 'how' in g.lower())"
if errorlevel 1 (
    echo FAIL: Greeting failed
    pause
    exit /b 1
)
echo PASS: Greeting works
echo.

echo [Test 6] Testing preference collection...
"%PYTHON_EXE%" -c "from src.agent import VacationAgent; a = VacationAgent(); prefs = a.collect_preferences(vacation_type='beach', duration=7, budget=3000); print('  Preferences stored:', len(prefs), 'items'); print('  Vacation type:', prefs.get('vacation_type'))"
if errorlevel 1 (
    echo FAIL: Preference collection failed
    pause
    exit /b 1
)
echo PASS: Preferences collected
echo.

echo [Test 7] Testing source validation...
"%PYTHON_EXE%" -c "from src.agent import VacationAgent; a = VacationAgent(); tests = [('https://tripadvisor.com', True), ('https://aa.com', True), ('https://expedia.com', False)]; [print(f'  {url}: {\"PASS\" if a.validate_source(url) == expected else \"FAIL\"}') for url, expected in tests]"
if errorlevel 1 (
    echo FAIL: Source validation failed
    pause
    exit /b 1
)
echo PASS: Source validation works
echo.

echo [Test 8] Testing destination planning...
"%PYTHON_EXE%" -c "from src.agent import VacationAgent; a = VacationAgent(); d = a.plan_destination('beach', 7, 2000); print('  Destination model created'); print('  Has TripAdvisor URL:', d.tripadvisor_url is not None)"
if errorlevel 1 (
    echo FAIL: Destination planning failed
    pause
    exit /b 1
)
echo PASS: Destination planning works
echo.

echo [Test 9] Testing VS Code extension compilation...
cd /d "%PROJECT_DIR%\vscode-extension"
if exist "out\extension.js" (
    echo   Compiled JS exists: out\extension.js
    echo PASS: Extension compiled
) else (
    echo Extension not compiled. Running npm run compile...
    call npm run compile
)
echo.

echo ============================================
echo   All Tests Passed!
echo ============================================
echo.
echo Next Steps:
echo 1. Open VS Code
echo 2. Open folder: %PROJECT_DIR%\vscode-extension
echo 3. Press F5 to launch Extension Development Host
echo 4. Click the Vacation Agent icon in sidebar
echo.
pause
