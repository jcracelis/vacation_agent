# vacation_agent 🌴

An AI-powered vacation planning agent specializing in **adult-only vacations** with verified information from trusted sources.

## Features

- ✅ Verified destination recommendations from TripAdvisor
- ✅ Custom itineraries for adult travelers
- ✅ Non-stop flights (aa.com, southwest.com, delta.com) and rail (amtrak.com) only
- ✅ Accurate budget estimates from approved sources
- ✅ Interactive VS Code extension with chat interface
- ✅ Source validation — no hallucination, all facts double-checked
- ✅ **Three LLM providers** — OpenAI, Qwen (Alibaba Cloud), and **Ollama (local, free, private)**

## LLM Providers

| Provider | Models | API Key | Cost | Privacy | Best For |
|----------|--------|---------|------|---------|----------|
| **Ollama** (default) | llama3, mistral, phi3, qwen2, gemma2 | None — local | Free | 100% local | Privacy, offline use, no costs |
| **OpenAI** | gpt-4, gpt-4-turbo, gpt-3.5-turbo | `OPENAI_API_KEY` | Per-token | Cloud | Best reasoning quality |
| **Qwen** | qwen-plus, qwen-max, qwen-turbo | `QWEN_API_KEY` | Per-token | Cloud | Cost-effective, multilingual |

Auto-detection priority: **Ollama → Qwen → OpenAI** (first available wins). Override with `vacationAgent.llmProvider` in settings.

## Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| **Python** | 3.10+ | Agent backend |
| **Node.js** | 18+ | VS Code extension build |
| **VS Code** | 1.85+ | Extension runtime |
| **Ollama** (optional) | Latest | Local LLM — no API key needed |
| **OpenAI API Key** (optional) | — | GPT-4 / GPT-3.5-turbo responses |
| **Qwen API Key** (optional) | — | Qwen responses (Alibaba Cloud DashScope) |

## Quick Start

### Windows (One-Click Setup)

Double-click `.github\agents\setup.bat` — it installs Python dependencies, compiles the extension, checks for Ollama, and opens VS Code.

Then in VS Code: **F5** → click 🌴 Vacation Agent icon → chat!

### Manual Setup

#### Step 1: Install Python Dependencies

```bash
cd .github/agents
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Set Up VS Code Extension

```bash
cd .github/agents/vscode-extension
npm install
npm run compile
```

### Step 3: Choose Your LLM Provider

#### Option A: Ollama (Recommended — free, local, private)

1. Install Ollama: https://ollama.com
2. Pull a model: `ollama pull llama3`
3. Start the server: `ollama serve`
4. No API key needed — it just works!

#### Option B: OpenAI

1. Get an API key: https://platform.openai.com/api-keys
2. Set in VS Code: `vacationAgent.openaiApiKey` → `sk-your-key`
3. Or set env var: `export OPENAI_API_KEY=sk-your-key`

#### Option C: Qwen (Alibaba Cloud)

1. Get an API key: https://dashscope.console.aliyun.com/
2. Set in VS Code: `vacationAgent.qwenApiKey` → `your-key`
3. Or set env var: `export QWEN_API_KEY=your-key`

### Step 4: Launch

1. Open VS Code: `code .github/agents/vscode-extension`
2. Press `F5` to launch Extension Development Host
3. Click the 🌴 Vacation Agent icon in the sidebar
4. Start chatting with your vacation planner!

## Project Structure

```
vacation_agent/
├── README.md                      # This file
├── .github/
│   └── agents/                    # All agents live here
│       ├── README.md              # Detailed install guide
│       ├── src/                   # Python source code
│       │   ├── agent.py           # Main agent (OpenAI + Qwen + Ollama)
│       │   ├── models.py          # Data models
│       │   ├── prompts.py         # Prompt templates
│       │   └── utils.py           # Utility functions
│       ├── tests/                 # Test suite (34 tests)
│       ├── config/                # Configuration files
│       ├── examples/              # Usage examples
│       ├── docs/                  # Documentation
│       ├── notebooks/             # Jupyter notebooks
│       ├── scripts/               # Utility scripts
│       ├── vscode-extension/      # VS Code extension
│       │   ├── src/               # TypeScript source
│       │   └── python_wrapper.py  # Python bridge (3 providers)
│       ├── validate.sh            # 8-point validation script
│       └── test_agent.bat         # Windows test script
```

## Configuration

Open VS Code Settings (`Ctrl+,`) and configure:

| Setting | Default | Description |
|---------|---------|-------------|
| `vacationAgent.pythonPath` | `python` | Path to Python executable |
| `vacationAgent.projectPath` | _(empty)_ | Path to the `agents/` directory |
| `vacationAgent.llmProvider` | `ollama` | `openai`, `qwen`, or `ollama` |
| `vacationAgent.openaiApiKey` | _(empty)_ | OpenAI API key |
| `vacationAgent.qwenApiKey` | _(empty)_ | Qwen DashScope API key |
| `vacationAgent.ollamaBaseUrl` | `http://localhost:11434` | Ollama server URL |

## Useful Scripts

| Script | Platform | Purpose |
|--------|----------|---------|
| `validate.sh` | WSL/Linux | 8-point code validation |
| `test_agent.bat` | Windows | Run test suite |

```bash
cd .github/agents
bash validate.sh
```

## Adding New Agents

To add a new agent:

1. Create a folder under `.github/agents/agent_name/`
2. Follow the standard structure (see Project Structure above)
3. Update this README with the new agent details

### Agent Requirements

- Python 3.10+ compatible
- Pydantic for data models
- Test coverage > 80%
- Comprehensive README
- Passes `validate.sh`

## License

MIT
