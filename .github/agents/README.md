# Vacation Agent

An AI-powered vacation planning agent specializing in **adult-only vacations**. All recommendations are grounded in verified information from trusted sources — no hallucination, no made-up prices.

## Features

- 🌴 **Destination Recommendations** — verified via TripAdvisor reviews
- ✈️ **Transportation Search** — non-stop flights only (aa.com, southwest.com, delta.com) and rail (amtrak.com)
- 📋 **Day-by-Day Itineraries** — logical, personalized planning
- 💰 **Budget Estimates** — sourced from approved carrier websites
- 🔍 **Source Validation** — every suggestion is verified before presentation
- 🤖 **Three LLM Providers** — OpenAI, Qwen (Alibaba Cloud), and Ollama (local)

## Agent Behavior Rules

1. **Adult-only focus** — All suggestions are appropriate for adult travelers
2. **Verified sources only** — TripAdvisor for reviews, carrier websites for transportation
3. **Warm, friendly tone** — Conversational, not robotic
4. **Ask clarifying questions** — Understand preferences before recommending
5. **Consider travel time** — Realistic scheduling with buffer
6. **No hallucination** — If unsure, say so
7. **Double-check everything** — Validate before presenting

## Installation

### Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| **Python** | 3.10+ | Agent backend |
| **Node.js** | 18+ | VS Code extension build |
| **VS Code** | 1.85+ | Extension runtime |

### LLM Providers

The agent supports three LLM providers. You only need to configure one.

| Provider | Models | API Key | Cost | Privacy | Setup |
|----------|--------|---------|------|---------|-------|
| **Ollama** (default) | llama3, mistral, phi3, qwen2, gemma2, deepseek-r1 | None | Free | 100% local | See below |
| **OpenAI** | gpt-4, gpt-4-turbo, gpt-3.5-turbo | `OPENAI_API_KEY` | Per-token | Cloud | https://platform.openai.com/api-keys |
| **Qwen** | qwen-plus, qwen-max, qwen-turbo, qwen-long | `QWEN_API_KEY` | Per-token | Cloud | https://dashscope.console.aliyun.com/ |

**Auto-detection:** If no provider is explicitly set, the agent checks in this order: **Ollama → Qwen → OpenAI** (first available wins).

### Step 1: Install Python Dependencies

```bash
cd .github/agents

# Create virtual environment (recommended)
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Set Up VS Code Extension

```bash
cd vscode-extension
npm install
npm run compile
```

### Step 3: Configure VS Code Extension

1. Open the `vscode-extension` folder in VS Code
2. Open Settings: `Ctrl+,` (Windows/Linux) or `Cmd+,` (Mac)
3. Search for "Vacation Agent"

   | Setting | Value | Description |
   |---------|-------|-------------|
   | **Project Path** | Path to `agents/` directory | Full absolute path |
   | **Python Path** | `python`, `python3`, or full path | Your Python executable |
   | **LLM Provider** | `ollama` (default), `openai`, `qwen` | Choose your LLM |
   | **OpenAI API Key** | _(optional)_ | Or set `OPENAI_API_KEY` env var |
   | **Qwen API Key** | _(optional)_ | Or set `QWEN_API_KEY` env var |
   | **Ollama Base URL** | `http://localhost:11434` | Your Ollama server URL |

   **Windows Example (Ollama):**
   ```
   Project Path: C:\Users\yourname\github\vacation_agent\.github\agents
   Python Path: C:\Program Files\Python314\python.exe
   LLM Provider: ollama
   Ollama Base URL: http://localhost:11434
   ```

   **Windows Example (OpenAI):**
   ```
   Project Path: C:\Users\yourname\github\vacation_agent\.github\agents
   Python Path: C:\Program Files\Python314\python.exe
   LLM Provider: openai
   OpenAI API Key: sk-your-key-here
   ```

   **Linux/Mac Example:**
   ```
   Project Path: /home/user/github/vacation_agent/.github/agents
   Python Path: python3
   LLM Provider: ollama
   ```

   **Or edit settings.json directly:**
   ```json
   {
     "vacationAgent.projectPath": "/path/to/vacation_agent/.github/agents",
     "vacationAgent.pythonPath": "python3",
     "vacationAgent.llmProvider": "ollama",
     "vacationAgent.ollamaBaseUrl": "http://localhost:11434",
     "vacationAgent.openaiApiKey": "",
     "vacationAgent.qwenApiKey": ""
   }
   ```

### Step 4: Launch

1. Open the `vscode-extension` folder in VS Code
2. Press `F5` (launches Extension Development Host)
3. In the new window:
   - Click the 🌴 Vacation Agent icon (left sidebar)
   - Or `Ctrl+Shift+P` → "Vacation Agent: Start Planning"
4. Begin chatting!

### Step 5: Set Up Ollama (Optional — Recommended)

Ollama runs LLMs locally on your machine — no API keys, no cloud costs, 100% private.

1. **Install Ollama:** https://ollama.com
2. **Pull a model:**
   ```bash
   ollama pull llama3        # General purpose (recommended)
   ollama pull mistral       # Fast and capable
   ollama pull phi3          # Lightweight
   ollama pull qwen2         # Great multilingual support
   ```
3. **Start the server:**
   ```bash
   ollama serve              # Runs on localhost:11434
   ```
4. **That's it!** No API key needed. The agent auto-detects Ollama and uses it by default.

### Step 6: Set API Keys (Optional — for Cloud Providers)

If you're using OpenAI or Qwen instead of Ollama:

#### Option A: VS Code Settings

Open Settings (`Ctrl+,`), search for "Vacation Agent", and set:
- `llmProvider`: `"openai"` or `"qwen"`
- `openaiApiKey`: Your OpenAI key
- `qwenApiKey`: Your Qwen (DashScope) key

#### Option B: Environment Variables

```bash
# Linux/Mac
export OPENAI_API_KEY="sk-your-api-key-here"
export QWEN_API_KEY="your-dashscope-key-here"

# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-your-api-key-here"
$env:QWEN_API_KEY="your-dashscope-key"

# Or add to .env file in agents root:
OPENAI_API_KEY=sk-your-api-key-here
QWEN_API_KEY=your-dashscope-key
```

## Usage

### VS Code Extension (Recommended)

#### Commands

Open Command Palette (`Ctrl+Shift+P`):
- **Vacation Agent: Start Planning** — Start a new planning session
- **Vacation Agent: Clear Chat** — Clear conversation history

#### Chat Interface

1. Click the Vacation Agent icon in the Activity Bar
2. Answer the agent's clarifying questions
3. Receive verified destination recommendations

### Python API

```python
from src.agent import VacationAgent

# OpenAI
agent = VacationAgent(provider="openai", openai_api_key="sk-your-key")

# Qwen
agent = VacationAgent(provider="qwen", qwen_api_key="your-key")

# Ollama (local)
agent = VacationAgent(provider="ollama", model_name="llama3")

# Greet
greeting = agent.greet()

# Chat
response = agent.chat("I want a romantic beach getaway for 7 days")

# Plan destination
result = agent.plan_destination("beach", duration_days=7, budget=3000)

# Find transportation
transport = agent.find_transportation("Chicago", "Miami", "2026-05-15")

# Suggest activities
activities = agent.suggest_activities("Cancun", "beach", 7)

# Generate itinerary
itinerary = agent.generate_itinerary("Cancun", 7)

# Estimate budget
budget = agent.estimate_budget("Cancun", 7, 2)
```

### CLI Usage

```bash
cd .github/agents

# Set environment variables (optional)
export OPENAI_API_KEY=sk-your-key     # or
export QWEN_API_KEY=your-key          # or start Ollama

# Run the agent directly
python -m src.agent

# Or via wrapper
cd vscode-extension
python python_wrapper.py greet
python python_wrapper.py chat "I want a beach vacation"
```

## Project Structure

```
agents/
├── README.md                   # This file
├── src/
│   ├── agent.py                # Main VacationAgent class (3 providers)
│   ├── models.py               # Pydantic data models
│   ├── prompts.py              # System and interaction prompts
│   └── utils.py                # Utility functions
├── tests/
│   └── test_agent.py           # Test suite (34 tests)
├── config/                     # Configuration files
├── examples/                   # Usage examples
├── docs/                       # Documentation
├── notebooks/                  # Jupyter notebooks
├── scripts/                    # Helper scripts
├── vscode-extension/
│   ├── src/
│   │   ├── extension.ts                # VS Code extension entry point
│   │   ├── VacationAgentViewProvider.ts # Webview chat panel
│   │   └── PythonAgentBridge.ts        # Python subprocess bridge
│   ├── out/                    # Compiled JavaScript
│   ├── media/
│   │   ├── chat.css            # Chat UI styles
│   │   └── chat.js             # Chat UI logic
│   ├── python_wrapper.py       # Python wrapper (multi-provider)
│   ├── .vscode/
│   │   └── settings.json       # Default configuration
│   ├── package.json            # Extension manifest
│   └── tsconfig.json           # TypeScript configuration
├── validate.sh                 # 8-point validation script
└── test_agent.bat              # Windows test script
```

## How the LLM Generates Responses

### With Ollama (Local)

When you send a message, here's what happens:

```
You type: "I want a beach vacation for 7 days"
          ↓
VS Code Extension (TypeScript)
  → Spawns python_wrapper.py as a subprocess
  → Passes your message via command-line argument
          ↓
Python VacationAgent
  → Wraps your message in the conversation history
  → Sends a POST request to http://localhost:11434/v1/chat/conversations
  → Payload: { model: "llama3", messages: [...], temperature: 0.7 }
          ↓
Ollama Server (Local)
  → Loads the llama3 model into memory
  → Processes your prompt through the neural network
  → Generates token-by-token response
  → Returns JSON: { choices: [{ message: { content: "..." } }] }
          ↓
Python VacationAgent
  → Parses the response
  → Validates any cited sources against approved domains
  → Returns formatted text back to VS Code
          ↓
VS Code Extension
  → Displays the response in the chat panel
```

**Key points about Ollama:**
- **Runs locally** on your machine — no data leaves your computer
- **No API key or internet** required after model download
- **Model stored** in `~/.ollama/models/` (typically 4–8 GB for llama3)
- **Response time** depends on your hardware (faster with GPU)
- **Privacy**: Your vacation preferences never leave your device

### With Cloud Providers (OpenAI / Qwen)

The flow is identical except:
- Request goes to `api.openai.com` or `dashscope.aliyuncs.com`
- Requires a valid API key
- Data is sent to the cloud provider's servers
- Response time is typically faster than local Ollama

### Source Verification

Every response is grounded in the agent's system prompt which requires:
- Destination reviews must cite tripadvisor.com
- Flight info must come from aa.com, southwest.com, or delta.com
- Rail info must come from amtrak.com
- The LLM is instructed: "DO NOT hallucinate information"

## Troubleshooting

### "Python not found"

Open Settings → Search "Vacation Agent: Python Path" → Set to your Python executable.

### "Project path not found"

Open Settings → Search "Vacation Agent: Project Path" → Set to the absolute path of your `agents/` directory.

### "Cannot connect to Ollama"

1. Make sure Ollama is installed: https://ollama.com
2. Start the server: `ollama serve`
3. Pull a model: `ollama pull llama3`
4. If Ollama runs on a different port, update `vacationAgent.ollamaBaseUrl`

### No LLM responses

1. Check your provider is configured correctly
2. For cloud providers: verify your API key is set
3. For Ollama: verify the server is running (`ollama serve`)
4. Check the VS Code Developer Tools for errors: `Help > Toggle Developer Tools`

### TypeScript compilation errors

```bash
cd vscode-extension
npm install
npm run compile
```

## Development

### Watch Mode

```bash
cd vscode-extension
npm run watch
```

### Validation

```bash
cd .github/agents
bash validate.sh
```

### Run Tests

```bash
cd .github/agents
python -m pytest tests/ -v
```

## License

MIT
