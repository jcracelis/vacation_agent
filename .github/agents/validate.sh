#!/bin/bash
# ============================================================================
# Vacation Agent - Validation Script (WSL)
# ============================================================================
# Purpose: Validates code structure, compilation, configuration, and behavior
#          rules for the Vacation Agent project.
#
# This script performs 8 comprehensive validation checks:
#   1. File Structure       - Verifies all required project files exist
#   2. TypeScript Compile   - Validates VS Code extension compilation
#   3. Package.json         - Parses and validates extension manifest
#   4. VS Code Settings     - Checks required vacation agent configurations
#   5. Python Syntax        - Runs py_compile on all Python source files
#   6. Agent Imports      - Validates key imports and method existence
#   7. Behavior Rules       - grep-based checks for prompt content requirements
#   8. Test Suite           - Counts and validates test methods
#
# Usage: ./validate.sh
# Requirements: bash, grep, python3, node, npm
# ============================================================================

# Configuration
PROJECT="/mnt/c/Users/racel/github/vacation_agent/.github/agents"
VSCODE_EXT="$PROJECT/vscode-extension"
PYTHON="/mnt/c/Program Files/Python314/python.exe"

# Trackers
PASS_COUNT=0
FAIL_COUNT=0

# ============================================================================
# Helper Functions
# ============================================================================

# print_header() - Display the validation report header
print_header() {
    echo "============================================"
    echo "  Vacation Agent - Validation Report"
    echo "============================================"
    echo ""
}

# print_footer() - Display completion summary
print_footer() {
    echo "============================================"
    echo "  Validation Complete!"
    echo "============================================"
    echo ""
    echo "Results: $PASS_COUNT passed, $FAIL_COUNT failed"
    echo ""
}

# print_pass() - Record and display a passing check
# Arguments:
#   $1 - Check description
print_pass() {
    echo "  ✅ $1"
    PASS_COUNT=$((PASS_COUNT + 1))
}

# print_fail() - Record and display a failing check
# Arguments:
#   $1 - Check description
print_fail() {
    echo "  ❌ $1"
    FAIL_COUNT=$((FAIL_COUNT + 1))
}

# print_info() - Display informational message
# Arguments:
#   $1 - Info message
print_info() {
    echo "  $1"
}

# print_usage_instructions() - Show VS Code setup guide
print_usage_instructions() {
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
}

# ============================================================================
# Validation Functions
# ============================================================================

# check_file_structure() - Verify all required project files exist
# Checks for Python sources, tests, config, and VS Code extension files
check_file_structure() {
    echo "[1/8] Checking file structure..."
    local FILES_OK=true
    local REQUIRED_FILES=(
        "src/agent.py" "src/models.py" "src/prompts.py" "src/utils.py"
        "tests/test_agent.py" "config/settings.yaml" "requirements.txt"
        "vscode-extension/src/extension.ts" "vscode-extension/package.json"
        "vscode-extension/media/chat.css" "vscode-extension/media/chat.js"
        "vscode-extension/.vscode/settings.json"
    )

    for f in "${REQUIRED_FILES[@]}"; do
        if [ ! -f "$PROJECT/$f" ]; then
            print_fail "Missing: $f"
            FILES_OK=false
        fi
    done

    if $FILES_OK; then
        print_pass "All required files present"
    fi
    echo ""
}

# check_typescript_compilation() - Validate VS Code extension compilation
# Runs npm run compile and checks for output file
check_typescript_compilation() {
    echo "[2/8] Checking TypeScript compilation..."
    cd "$VSCODE_EXT" || return

    if npm run compile > /dev/null 2>&1; then
        print_pass "TypeScript compiles successfully"
        if [ -f "out/extension.js" ]; then
            print_pass "Output file exists: out/extension.js"
        else
            print_fail "Output file missing: out/extension.js"
        fi
    else
        print_fail "TypeScript compilation failed"
    fi
    echo ""
}

# validate_package_json() - Parse and validate extension manifest
# Checks package.json syntax and extracts extension metadata
validate_package_json() {
    echo "[3/8] Validating package.json..."
    cd "$VSCODE_EXT" || return

    if node -e "const p = require('./package.json'); console.log('  Extension:', p.displayName); console.log('  Version:', p.version); console.log('  Commands:', p.contributes.commands.length);" 2>/dev/null; then
        print_pass "package.json is valid"
    else
        print_fail "package.json has errors"
    fi
    echo ""
}

# check_vscode_settings() - Verify required VS Code configurations
# Checks for vacationAgent.pythonPath and vacationAgent.projectPath settings
check_vscode_settings() {
    echo "[4/8] Checking VS Code settings..."
    local SETTINGS="$VSCODE_EXT/.vscode/settings.json"

    if [ -f "$SETTINGS" ]; then
        local PYTHON_PATH PROJECT_PATH
        PYTHON_PATH=$(grep -o '"vacationAgent.pythonPath"[[:space:]]*:[[:space:]]*"[^"]*"' "$SETTINGS" | cut -d'"' -f4)
        PROJECT_PATH=$(grep -o '"vacationAgent.projectPath"[[:space:]]*:[[:space:]]*"[^"]*"' "$SETTINGS" | cut -d'"' -f4)
        print_info "Python Path: $PYTHON_PATH"
        print_info "Project Path: $PROJECT_PATH"
        print_pass "Settings configured"
    else
        print_fail "Settings file missing"
    fi
    echo ""
}

# check_python_syntax() - Validate Python source file syntax
# Runs py_compile on all Python source and test files
check_python_syntax() {
    echo "[5/8] Validating Python syntax..."
    local SYNTAX_OK=true
    local PYTHON_FILES=("src/agent.py" "src/models.py" "src/prompts.py" "src/utils.py" "tests/test_agent.py")

    for f in "${PYTHON_FILES[@]}"; do
        if python3 -m py_compile "$PROJECT/$f" 2>/dev/null; then
            print_pass "$f"
        else
            print_fail "$f"
            SYNTAX_OK=false
        fi
    done
    echo ""
}

# check_agent_imports() - Validate key imports and method existence
# Checks for prompts import, pydantic, APPROVED_REVIEW_SOURCES, and validate_source
check_agent_imports() {
    echo "[6/8] Checking agent imports..."
    cd "$PROJECT" || return

    if grep -q "from src.prompts import" src/agent.py; then
        print_pass "Prompts imported"
    fi
    if grep -q "from pydantic import" src/agent.py; then
        print_pass "Pydantic imported"
    fi
    if grep -q "APPROVED_REVIEW_SOURCES" src/agent.py; then
        print_pass "Approved sources defined"
    fi
    if grep -q "validate_source" src/agent.py; then
        print_pass "Source validation method exists"
    fi
    echo ""
}

# check_behavior_rules() - Validate agent behavior rules in prompts.py
# Uses grep to verify required content: adult-only, TripAdvisor, airlines, anti-hallucination
check_behavior_rules() {
    echo "[7/8] Validating agent behavior rules..."

    if grep -q "adult only vacations" src/prompts.py; then
        print_pass "Adult-only focus"
    fi
    if grep -q "tripadvisor.com" src/prompts.py; then
        print_pass "TripAdvisor source requirement"
    fi
    if grep -q "aa.com" src/prompts.py && grep -q "southwest.com" src/prompts.py && grep -q "delta.com" src/prompts.py; then
        print_pass "Airline sources defined"
    fi
    if grep -q "amtrak.com" src/prompts.py; then
        print_pass "Rail source defined"
    fi
    if grep -q "non-stop" src/prompts.py; then
        print_pass "Non-stop flight requirement"
    fi
    if grep -q "DO NOT hallucinate" src/prompts.py; then
        print_pass "Anti-hallucination rule"
    fi
    if grep -q "double-check" src/prompts.py; then
        print_pass "Double-check requirement"
    fi
    echo ""
}

# check_test_suite() - Validate test suite completeness
# Counts test methods in test_agent.py and validates minimum threshold
check_test_suite() {
    echo "[8/8] Checking test suite..."
    local TEST_COUNT
    TEST_COUNT=$(grep -c "def test_" tests/test_agent.py)
    print_info "Test methods found: $TEST_COUNT"

    if [ "$TEST_COUNT" -ge 10 ]; then
        print_pass "Comprehensive test suite"
    else
        echo "  ⚠️  Consider adding more tests"
    fi
    echo ""
}

# ============================================================================
# Main Execution
# ============================================================================

print_header

# Run all validation checks sequentially
check_file_structure
check_typescript_compilation
validate_package_json
check_vscode_settings
check_python_syntax
check_agent_imports
check_behavior_rules
check_test_suite

print_footer
print_usage_instructions
