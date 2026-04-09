# Vacation Agent VS Code Extension

Integrate the AI-powered adult-only vacation planner directly into VS Code.

## Features

- 💬 **Chat Interface** — Interactive chat panel in VS Code sidebar
- 🌴 **Vacation Planning** — Destination recommendations from TripAdvisor
- ✈️ **Transportation Search** — Non-stop flights and rail options
- 📋 **Itinerary Generation** — Detailed day-by-day plans
- 💰 **Budget Estimates** — Verified pricing from approved sources
- 🔍 **Source Validation** — All recommendations verified before presentation
- 🤖 **Three LLM Providers** — Ollama (local, free), OpenAI (GPT-4), Qwen (Alibaba Cloud)

## Requirements

- **VS Code 1.85+**
- **Node.js 18+** — For building the extension
- **Python 3.10+** — For the vacation agent backend
- **Ollama** (recommended, optional) — For local LLM: https://ollama.com

## Installation

### Option 1: Development Installation

1. **Install dependencies**
   ```bash
   cd vscode-extension
   npm install
   ```

2. **Compile**
   ```bash
   npm run compile
   ```

3. **Run** — Open the `vscode-extension` folder in VS Code, press `F5`

4. **Access** — Click the Vacation Agent icon in the Activity Bar, or:
   `Ctrl+Shift+P` → "Vacation Agent: Start Planning"

### Option 2: Package as VSIX

```bash
npm install -g @vscode/vsce
vsce package
code --install-extension vacation-agent-<version>.vsix
```

## Configuration

Open VS Code Settings (`Ctrl+,`):

### Required

| Setting | Description | Example |
|---------|-------------|---------|
| **Project Path** | Path to `agents/` directory | `C:\Users\you\github\vacation_agent\.github\agents` |
| **Python Path** | Python executable | `C:\Program Files\Python314\python.exe` or `python3` |

### LLM Provider

| Setting | Values | Default | Description |
|---------|--------|---------|-------------|
| **LLM Provider** | `ollama`, `openai`, `qwen` | `ollama` | Choose your LLM |
| **Ollama Base URL** | URL | `http://localhost:11434` | Ollama server address |
| **OpenAI API Key** | String | _(empty)_ | OpenAI key or `OPENAI_API_KEY` env var |
| **Qwen API Key** | String | _(empty)_ | DashScope key or `QWEN_API_KEY` env var |

### Example: Ollama (Local, Free)

```json
{
  "vacationAgent.llmProvider": "ollama",
  "vacationAgent.ollamaBaseUrl": "http://localhost:11434"
}
```

### Example: OpenAI

```json
{
  "vacationAgent.llmProvider": "openai",
  "vacationAgent.openaiApiKey": "sk-your-key-here"
}
```

### Example: Qwen

```json
{
  "vacationAgent.llmProvider": "qwen",
  "vacationAgent.qwenApiKey": "your-dashscope-key"
}
```

## Usage

### Commands

| Command | Palette Name | Description |
|---------|-------------|-------------|
| `vacationAgent.startPlanning` | Vacation Agent: Start Planning | New planning session |
| `vacationAgent.clearChat` | Vacation Agent: Clear Chat | Clear conversation |

### Chat Flow

```
Agent: Hello! I'm your adult-only vacation planner. What type of vacation
       are you dreaming of?

You: I'm looking for a romantic beach getaway for 7 days

Agent: Wonderful! Let me find some verified options from TripAdvisor...
       [presents destination, cost, highlights]
```

## Project Structure

```
vscode-extension/
├── src/
│   ├── extension.ts                  # Extension entry point
│   ├── VacationAgentViewProvider.ts  # Webview chat panel
│   └── PythonAgentBridge.ts          # Python subprocess bridge
├── out/                              # Compiled JavaScript (generated)
├── media/
│   ├── chat.css                      # Chat styles
│   ├── chat.js                       # Chat UI logic
│   └── icon.svg                      # Extension icon
├── python_wrapper.py                 # Python wrapper (3 providers)
├── .vscode/
│   └── settings.json                 # Default configuration
├── package.json                      # Extension manifest
├── tsconfig.json                     # TypeScript config
└── README.md                         # This file
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Python not found" | Set `vacationAgent.pythonPath` in settings |
| "Project path not found" | Set `vacationAgent.projectPath` to absolute path |
| No response from agent | Check Python deps: `pip install -r requirements.txt` |
| "Cannot connect to Ollama" | Run `ollama serve` and `ollama pull llama3` |
| TypeScript errors | Run `npm install && npm run compile` |
| Developer errors | `Help > Toggle Developer Tools` → Console tab |

## Development

```bash
# Watch mode (auto-recompile)
npm run watch

# Lint
npm run lint

# Package
vsce package
```

## License

MIT

## Support

https://github.com/jcracelis/vacation_agent/issues
