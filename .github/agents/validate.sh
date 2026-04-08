#!/bin/bash
# Vacation Agent - Validation Script (WSL)
# Validates code structure, compilation, and configuration

PROJECT="/mnt/c/Users/racel/github/vacation_agent/.github/agents"
VSCODE_EXT="$PROJECT/vscode-extension"
PYTHON="/mnt/c/Program Files/Python314/python.exe"

echo "============================================"
echo "  Vacation Agent - Validation Report"
echo "============================================"
echo ""

# Test 1: File Structure
echo "[1/8] Checking file structure..."
FILES_OK=true
for f in src/agent.py src/models.py src/prompts.py src/utils.py \
         tests/test_agent.py config/settings.yaml requirements.txt \
         vscode-extension/src/extension.ts vscode-extension/package.json \
         vscode-extension/media/chat.css vscode-extension/media/chat.js \
         vscode-extension/.vscode/settings.json; do
    if [ ! -f "$PROJECT/$f" ]; then
        echo "  ❌ Missing: $f"
        FILES_OK=false
    fi
done
if $FILES_OK; then
    echo "  ✅ All required files present"
fi
echo ""

# Test 2: TypeScript Compilation
echo "[2/8] Checking TypeScript compilation..."
cd "$VSCODE_EXT"
if npm run compile > /dev/null 2>&1; then
    echo "  ✅ TypeScript compiles successfully"
    if [ -f "out/extension.js" ]; then
        echo "  ✅ Output file exists: out/extension.js"
    fi
else
    echo "  ❌ TypeScript compilation failed"
fi
echo ""

# Test 3: Package.json validation
echo "[3/8] Validating package.json..."
cd "$VSCODE_EXT"
if node -e "const p = require('./package.json'); console.log('  Extension:', p.displayName); console.log('  Version:', p.version); console.log('  Commands:', p.contributes.commands.length);" 2>/dev/null; then
    echo "  ✅ package.json is valid"
else
    echo "  ❌ package.json has errors"
fi
echo ""

# Test 4: VS Code settings
echo "[4/8] Checking VS Code settings..."
SETTINGS="$VSCODE_EXT/.vscode/settings.json"
if [ -f "$SETTINGS" ]; then
    PYTHON_PATH=$(grep -o '"vacationAgent.pythonPath"[[:space:]]*:[[:space:]]*"[^"]*"' "$SETTINGS" | cut -d'"' -f4)
    PROJECT_PATH=$(grep -o '"vacationAgent.projectPath"[[:space:]]*:[[:space:]]*"[^"]*"' "$SETTINGS" | cut -d'"' -f4)
    echo "  Python Path: $PYTHON_PATH"
    echo "  Project Path: $PROJECT_PATH"
    echo "  ✅ Settings configured"
else
    echo "  ❌ Settings file missing"
fi
echo ""

# Test 5: Python syntax check
echo "[5/8] Validating Python syntax..."
SYNTAX_OK=true
for f in src/agent.py src/models.py src/prompts.py src/utils.py tests/test_agent.py; do
    if python3 -m py_compile "$PROJECT/$f" 2>/dev/null; then
        echo "  ✅ $f"
    else
        echo "  ❌ $f"
        SYNTAX_OK=false
    fi
done
echo ""

# Test 6: Check imports in agent.py
echo "[6/8] Checking agent imports..."
cd "$PROJECT"
if grep -q "from src.prompts import" src/agent.py; then
    echo "  ✅ Prompts imported"
fi
if grep -q "from pydantic import" src/agent.py; then
    echo "  ✅ Pydantic imported"
fi
if grep -q "APPROVED_REVIEW_SOURCES" src/agent.py; then
    echo "  ✅ Approved sources defined"
fi
if grep -q "validate_source" src/agent.py; then
    echo "  ✅ Source validation method exists"
fi
echo ""

# Test 7: Verify behavior rules in prompts
echo "[7/8] Validating agent behavior rules..."
if grep -q "adult only vacations" src/prompts.py; then
    echo "  ✅ Adult-only focus"
fi
if grep -q "tripadvisor.com" src/prompts.py; then
    echo "  ✅ TripAdvisor source requirement"
fi
if grep -q "aa.com" src/prompts.py && grep -q "southwest.com" src/prompts.py && grep -q "delta.com" src/prompts.py; then
    echo "  ✅ Airline sources defined"
fi
if grep -q "amtrak.com" src/prompts.py; then
    echo "  ✅ Rail source defined"
fi
if grep -q "non-stop" src/prompts.py; then
    echo "  ✅ Non-stop flight requirement"
fi
if grep -q "DO NOT hallucinate" src/prompts.py; then
    echo "  ✅ Anti-hallucination rule"
fi
if grep -q "double-check" src/prompts.py; then
    echo "  ✅ Double-check requirement"
fi
echo ""

# Test 8: Test suite validation
echo "[8/8] Checking test suite..."
TEST_COUNT=$(grep -c "def test_" tests/test_agent.py)
echo "  Test methods found: $TEST_COUNT"
if [ "$TEST_COUNT" -ge 10 ]; then
    echo "  ✅ Comprehensive test suite"
else
    echo "  ⚠️  Consider adding more tests"
fi
echo ""

echo "============================================"
echo "  Validation Complete!"
echo "============================================"
echo ""
echo "📋 To test the agent in VS Code:"
echo ""
echo "1. Open VS Code"
echo "2. File → Open Folder → Select:"
echo "   C:\Users\racel\github\vacation_agent\.github\agents\vscode-extension"
echo ""
echo "3. Press F5 (launches Extension Development Host)"
echo ""
echo "4. In the new window:"
echo "   - Click the 🌴 Vacation Agent icon (left sidebar)"
echo "   - Or Ctrl+Shift+P → 'Vacation Agent: Start Planning'"
echo ""
echo "5. Configure if needed:"
echo "   - Ctrl+, → Search 'Vacation Agent'"
echo "   - Set Python path and project path"
echo ""
echo "6. Chat with your agent!"
echo ""
