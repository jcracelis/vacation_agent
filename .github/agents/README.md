# Vacation Agent 🌴

An AI-powered vacation planning agent specializing in **adult-only vacations** with verified information from trusted sources.

## Key Features

- 🌍 **Verified Destination Recommendations** - All suggestions grounded in TripAdvisor reviews
- 📅 **Custom Itineraries** - Personalized day-by-day plans for adult travelers
- ✈️ **Verified Transportation** - Non-stop flights (aa.com, southwest.com, delta.com) and rail (amtrak.com) only
- 💰 **Accurate Budget Estimates** - All pricing double-checked from approved sources
- 🔍 **Source Validation** - No hallucination; all information validated before presentation
- 💬 **Warm, Personal Service** - Clarifying questions to understand your preferences
- 🖥️ **VS Code Integration** - Interactive chat panel directly in your editor

## Trusted Sources

The agent uses **ONLY** these verified sources:
- **Reviews:** tripadvisor.com
- **Airlines:** aa.com, southwest.com, delta.com (non-stop flights only)
- **Rail:** amtrak.com

## Project Structure

```
vacation_agent/
├── src/                    # Source code
│   ├── __init__.py
│   ├── agent.py            # Main agent logic
│   ├── models.py           # Data models
│   ├── prompts.py          # Prompt templates
│   └── utils.py            # Utility functions
├── config/                 # Configuration files
│   └── settings.yaml
├── tests/                  # Test files
│   ├── __init__.py
│   └── test_agent.py
├── notebooks/              # Jupyter notebooks for exploration
├── docs/                   # Documentation
├── scripts/                # Utility scripts
├── vscode-extension/       # VS Code extension
│   ├── src/                # TypeScript source files
│   ├── media/              # UI assets (CSS, JS, icons)
│   ├── package.json        # Extension manifest
│   └── README.md           # Extension-specific docs
├── .gitignore
├── requirements.txt        # Python dependencies
├── setup.py                # Package setup
└── README.md
```

## Installation

### Prerequisites

- **Python 3.10+** - Required for the vacation agent backend
- **Node.js 18+** - Required for building the VS Code extension
- **VS Code 1.85+** - Minimum supported version
- **OpenAI API Key** (optional) - For LLM-powered responses

### Step 1: Install Python Dependencies

```bash
# From the repository root
cd ..

# Or clone the repository
git clone https://github.com/jcracelis/vacation_agent.git
cd vacation_agent/agents

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Set Up VS Code Extension

#### **Option A: Using the Setup Script (Recommended)**

```bash
# Run the automated setup script
./setup-vscode-extension.sh
```

This will:
- Verify Node.js installation
- Install extension dependencies
- Compile TypeScript
- Check Python availability

#### **Option B: Manual Setup**

```bash
cd vscode-extension

# Install dependencies
npm install

# Compile TypeScript
npm run compile
```

### Step 3: Configure the Extension

1. **Open the extension in VS Code:**
   ```bash
   code vscode-extension
   ```

2. **Launch the Extension Development Host:**
   - Press `F5` (or `Fn+F5` on some keyboards)
   - A new VS Code window will open titled "Extension Development Host"

3. **Configure Extension Settings:**
   - Press `Ctrl+,` (Windows/Linux) or `Cmd+,` (Mac) to open Settings
   - Search for "Vacation Agent"
   - Configure the following:

   | Setting | Value | Description |
   |---------|-------|-------------|
   | **Vacation Agent: Project Path** | `C:\Users\racel\github\vacation_agent\.github\agents` | Full path to this repository |
   | **Vacation Agent: Python Path** | `C:\Program Files\Python314\python.exe` | Your Python executable path |
   | **Vacation Agent: OpenAI API Key** | Your API key (optional) | Or set `OPENAI_API_KEY` env var |

   **Example Configuration:**
   ```
   Project Path: C:\Users\racel\github\vacation_agent\.github\agents
   Python Path: C:\Program Files\Python314\python.exe
   OpenAI API Key: sk-your-key-here (optional)
   ```

   **Alternative: Edit settings.json directly:**
   - Press `Ctrl+Shift+P` → Type "Preferences: Open Settings (JSON)"
   - Add:
   ```json
   {
     "vacationAgent.projectPath": "C:\\Users\\racel\\github\\vacation_agent\\.github\\agents",
     "vacationAgent.pythonPath": "C:\\Program Files\\Python314\\python.exe",
     "vacationAgent.openaiApiKey": "sk-your-api-key-here"
   }
   ```

### Step 4: Launch the Vacation Agent

1. **Access the Chat Panel:**
   - Look for the **🌴 Vacation Agent icon** in the Activity Bar (left sidebar)
   - Click it to open the chat panel

   **If you don't see the icon:**
   - Press `Ctrl+Shift+P` → Type "View: Show Vacation Agent"
   - Or: `View` → `Appearance` → `Show Activity Bar`

2. **Start a New Planning Session:**
   - Press `Ctrl+Shift+P` → Type "Vacation Agent: Start Planning"
   - The agent will greet you with clarifying questions

3. **Begin Chatting:**
   - Answer the agent's questions about your preferences
   - Receive verified recommendations from TripAdvisor and approved carriers

### Step 5: Set OpenAI API Key (Optional)

If you want to use LLM-powered responses:

**Method 1: VS Code Settings** (shown above in Step 3)

**Method 2: Environment Variable**
```bash
# Linux/Mac
export OPENAI_API_KEY="sk-your-api-key-here"

# Windows (Command Prompt)
set OPENAI_API_KEY=sk-your-api-key-here

# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-your-api-key-here"

# Or add to .env file in vacation_agent root:
echo "OPENAI_API_KEY=sk-your-api-key-here" > .env
```

**Get your API key:** https://platform.openai.com/api-keys

## Usage

### VS Code Extension (Recommended)

See the **Installation** section above for complete VS Code extension setup.

**Quick Start:**
1. Press `F5` in the `vscode-extension` folder
2. Click the 🌴 Vacation Agent icon in the sidebar
3. Chat with your vacation planner!

**Available Commands** (via `Ctrl+Shift+P`):
- **Vacation Agent: Start Planning** - Start a new planning session
- **Vacation Agent: Clear Chat** - Clear the conversation history

### Python API (Advanced)

```python
from src.agent import VacationAgent

# Initialize the agent
agent = VacationAgent()

# Send greeting and ask clarifying questions
greeting = agent.greet()
print(greeting)

# Collect preferences
agent.collect_preferences(
    vacation_type="romantic beach getaway",
    duration=7,
    budget=3000,
    origin="Chicago, IL",
    travel_dates="May 2026"
)

# Plan a destination (verified via TripAdvisor)
destination = agent.plan_destination("beach", 7, 3000)

# Find transportation (non-stop flights and rail only)
transport = agent.find_transportation("Chicago", "Miami", "2026-05-15")

# Validate all suggestions before presenting
validation = agent.validate_suggestions([destination])
```

## Troubleshooting

### Python Not Found

**Error:** "Python not found. Please configure the Python path in settings."

**Solution:**
1. Open VS Code Settings (`Ctrl+,` / `Cmd+,`)
2. Search for "Vacation Agent: Python Path"
3. Set the correct path:
   - Windows: `python` or `C:\Python310\python.exe`
   - Mac/Linux: `python3` or `/usr/bin/python3`

### Project Path Not Found

**Error:** "Project path not found: [path]"

**Solution:**
1. Open VS Code Settings
2. Search for "Vacation Agent: Project Path"
3. Set the **absolute path** to your vacation_agent directory
4. Example: `C:\Users\racel\github\vacation_agent\.github\agents`

### No Response from Agent

**Issue:** Agent doesn't respond or shows errors

**Solution:**
1. Verify Python dependencies: `pip install -r requirements.txt`
2. Check the project path is correct in settings
3. Open VS Code Developer Tools: `Help` → `Toggle Developer Tools`
4. Check the Console tab for errors

### Extension Icon Missing

**Issue:** Can't see the Vacation Agent icon in the sidebar

**Solution:**
1. Press `Ctrl+Shift+P` → Type "Developer: Reload Window"
2. Or: `View` → `Appearance` → Ensure "Activity Bar" is checked

### TypeScript Compilation Errors

**Error:** TypeScript compilation fails

**Solution:**
```bash
cd vscode-extension
rm -rf node_modules out
npm install
npm run compile
```

### Extension Development Host Not Loading

**Issue:** Pressing F5 doesn't open a new window

**Solution:**
1. Make sure you opened the `vscode-extension` folder (not the root)
2. Check for build errors in the Terminal panel
3. Run `npm run compile` manually
4. Try `View` → `Command Palette` → `Developer: Reload Window`

## Development

### Python Backend

```bash
# Run tests
pytest tests/

# Run linting
flake8 src/
```

### VS Code Extension

```bash
cd vscode-extension

# Watch mode (auto-recompile)
npm run watch

# Manual compile
npm run compile

# Lint
npm run lint
```

## License

MIT
