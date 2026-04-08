#!/bin/bash
# VS Code Extension Setup Script
# Run this script from the vacation_agent root directory

echo "🌴 Setting up Vacation Agent VS Code Extension..."
echo ""

# Navigate to extension directory
cd vscode-extension

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed."
    echo "   Please install Node.js from: https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js found: $(node --version)"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
npm install

# Compile TypeScript
echo ""
echo "🔨 Compiling TypeScript..."
npm run compile

# Check Python
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo ""
    echo "⚠️  Python not found in PATH."
    echo "   Please install Python 3.10+ and update vacationAgent.pythonPath in VS Code settings."
else
    PYTHON_CMD=$(command -v python &> /dev/null && echo "python" || echo "python3")
    echo ""
    echo "✅ Python found: $($PYTHON_CMD --version)"
fi

echo ""
echo "=========================================="
echo "✅ VS Code Extension Setup Complete!"
echo "=========================================="
echo ""
echo "📖 Next Steps:"
echo ""
echo "1. Open the extension folder in VS Code:"
echo "   code vscode-extension"
echo ""
echo "2. Press F5 to launch the Extension Development Host"
echo ""
echo "3. Configure the extension in VS Code Settings:"
echo "   - vacationAgent.projectPath: $(pwd)/../.."
echo "   - vacationAgent.pythonPath: python (or your Python path)"
echo "   - vacationAgent.openaiApiKey: (optional)"
echo ""
echo "4. Click the Vacation Agent icon in the Activity Bar"
echo ""
echo "For detailed instructions, see: vscode-extension/README.md"
echo ""
