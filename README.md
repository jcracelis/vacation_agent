# Agents Repository 🤖

A collection of AI-powered agents for various purposes.

## Available Agents

### 🌴 Vacation Agent

An AI-powered vacation planning agent specializing in **adult-only vacations** with verified information from trusted sources.

**Features:**
- ✅ Verified destination recommendations from TripAdvisor
- ✅ Custom itineraries for adult travelers
- ✅ Non-stop flights (aa.com, southwest.com, delta.com) and rail (amtrak.com) only
- ✅ Accurate budget estimates from approved sources
- ✅ Interactive VS Code extension with chat interface
- ✅ Source validation - no hallucination

📖 **[View Vacation Agent Documentation →](.github/agents/README.md)**

### Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| **Python** | 3.10+ | Agent backend |
| **Node.js** | 18+ | VS Code extension build |
| **VS Code** | 1.85+ | Extension runtime |
| **OpenAI API Key** | Optional | LLM-powered responses |

### Quick Start

#### **Step 1: Install Python Dependencies**

```bash
# From repository root
cd .github/agents

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### **Step 2: Set Up VS Code Extension**

```bash
# Navigate to extension
cd .github/agents/vscode-extension

# Install dependencies and compile
npm install
npm run compile
```

#### **Step 3: Launch**

1. Open VS Code: `code .github/agents/vscode-extension`
2. Press `F5` to launch Extension Development Host
3. Click the 🌴 Vacation Agent icon in the sidebar
4. Start chatting with your vacation planner!

📖 **[Full Installation Guide →](.github/agents/README.md#installation)**

## Project Structure

```
vacation_agent/                    # Repository root
├── README.md                      # This file
├── .github/
│   └── agents/                    # All agents live here
│       ├── README.md              # Vacation Agent documentation
│       ├── src/                   # Python source code
│       ├── tests/                 # Test suite
│       ├── config/                # Configuration files
│       ├── examples/              # Usage examples
│       ├── docs/                  # Documentation
│       ├── notebooks/             # Jupyter notebooks
│       ├── scripts/               # Utility scripts
│       ├── vscode-extension/      # VS Code extension
│       ├── validate.sh            # Validation script
│       └── test_agent.bat         # Windows test script
```

## Adding New Agents

To add a new agent to this repository:

1. **Create a folder** under `.github/agents/agent_name/`
2. **Follow the standard structure:**
   ```
   .github/agents/
   └── agent_name/
       ├── src/                     # Source code
       │   ├── __init__.py
       │   ├── agent.py             # Main agent logic
       │   ├── models.py            # Data models
       │   └── prompts.py           # Prompt templates
       ├── tests/                   # Test suite
       │   ├── __init__.py
       │   └── test_agent.py
       ├── config/                  # Configuration
       │   └── settings.yaml
       ├── examples/                # Usage examples
       ├── docs/                    # Documentation
       ├── notebooks/               # Jupyter notebooks
       ├── scripts/                 # Utility scripts
       ├── requirements.txt         # Python dependencies
       └── README.md                # Agent documentation
   ```
3. **Create a VS Code extension** (optional) following the `vscode-extension/` pattern
4. **Add tests** - minimum 10 test methods recommended
5. **Update this README** with the new agent details

### Agent Requirements

- **Python 3.10+** compatible
- **Pydantic** for data models
- **Test coverage** - aim for >80%
- **Documentation** - comprehensive README with setup instructions
- **Validation** - passes `validate.sh` script

## Useful Scripts

| Script | Platform | Purpose |
|--------|----------|---------|
| `validate.sh` | WSL/Linux | Comprehensive code validation |
| `test_agent.bat` | Windows | Run test suite on Windows |
| `setup-vscode-extension.sh` | WSL/Linux | Automated VS Code extension setup |

**Run validation:**
```bash
cd .github/agents
bash validate.sh
```

## License

MIT
