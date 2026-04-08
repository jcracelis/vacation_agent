# Vacation Agent VS Code Extension

Integrate the AI-powered adult-only vacation planner directly into VS Code.

## Features

- 💬 **Chat Interface** - Interactive chat panel in VS Code sidebar
- 🌴 **Vacation Planning** - Get destination recommendations from verified TripAdvisor sources
- ✈️ **Transportation Search** - Find non-stop flights and rail options
- 📋 **Itinerary Generation** - Create detailed day-by-day plans
- 💰 **Budget Estimates** - Accurate pricing from verified sources

## Installation

### Option 1: Development Installation (Recommended)

1. **Install Node.js** (if not already installed)
   - Download from: https://nodejs.org/

2. **Install dependencies**
   ```bash
   cd vscode-extension
   npm install
   ```

3. **Compile the extension**
   ```bash
   npm run compile
   ```

4. **Run the extension**
   - Open the `vscode-extension` folder in VS Code
   - Press `F5` to launch the Extension Development Host
   - A new VS Code window will open with the extension loaded

5. **Access the extension**
   - Click the Vacation Agent icon in the Activity Bar (left sidebar)
   - Or use Command Palette: `Ctrl+Shift+P` / `Cmd+Shift+P`
   - Type "Vacation Agent: Start Planning"

### Option 2: Package as VSIX

```bash
# Install vsce globally
npm install -g @vscode/vsce

# Package the extension
vsce package

# Install the .vsix file
code --install-extension vacation-agent-0.1.0.vsix
```

## Configuration

Open VS Code Settings (`Ctrl+,` / `Cmd+,`) and configure:

### Required Settings

1. **Vacation Agent: Project Path**
   - Path to the vacation_agent project directory
   - Example: `C:\Users\racel\github\vacation_agent\.github\agents`

2. **Vacation Agent: Python Path**
   - Path to your Python executable
   - Default: `C:\Program Files\Python314\python.exe`
   - Example: `python3` or full path like `C:\Program Files\Python314\python.exe`

3. **Vacation Agent: OpenAI API Key** (optional)
   - Your OpenAI API key
   - Can also be set via environment variable `OPENAI_API_KEY`

## Usage

### Commands

Access via Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`):

- **Vacation Agent: Start Planning** - Start a new planning session
- **Vacation Agent: Clear Chat** - Clear the conversation history

### Chat Interface

1. Click the Vacation Agent icon in the Activity Bar
2. The agent will greet you with clarifying questions
3. Answer questions about your preferences:
   - Vacation type (beach, mountains, city, etc.)
   - Duration
   - Budget
   - Travel dates
   - Origin location
4. Receive verified recommendations from TripAdvisor and approved carriers

### Example Conversation

```
Agent: Hello! I'm your adult-only vacation planner. What type of vacation are you dreaming of?

You: I'm looking for a romantic beach getaway for 7 days

Agent: Wonderful! Let me find some verified options from TripAdvisor...
```

## Requirements

- **Python 3.10+** - Required for the vacation agent backend
- **Node.js 18+** - Required for building the extension
- **VS Code 1.85+** - Minimum supported version
- **OpenAI API Key** - For LLM-powered responses (optional)

### Python Dependencies

Make sure the vacation_agent Python dependenciesies are installed:

```bash
cd /path/to/vacation_agent
pip install -r requirements.txt
```

## Project Structure

```
vscode-extension/
├── src/
│   ├── extension.ts                  # Main extension entry point
│   ├── VacationAgentViewProvider.ts  # Webview provider
│   └── PythonAgentBridge.ts          # Python process communication
├── media/
│   ├── chat.css                      # Chat interface styles
│   ├── chat.js                       # Chat interface logic
│   └── icon.svg                      # Extension icon
├── python_wrapper.py                 # Python script wrapper
├── package.json                      # Extension manifest
├── tsconfig.json                     # TypeScript configuration
└── README.md                         # This file
```

## Troubleshooting

### Python Not Found

**Error:** "Python not found. Please configure the Python path in settings."

**Solution:**
1. Open VS Code Settings
2. Search for "Vacation Agent: Python Path"
3. Set the correct path to your Python executable

### Project Path Not Found

**Error:** "Project path not found: [path]"

**Solution:**
1. Open VS Code Settings
2. Search for "Vacation Agent: Project Path"
3. Set the absolute path to your vacation_agent directory

### No Response from Agent

**Issue:** Agent doesn't respond or shows errors

**Solution:**
1. Check that Python dependencies are installed: `pip install -r requirements.txt`
2. Verify the project path is correct
3. Check the VS Code Developer Tools for errors: `Help > Toggle Developer Tools`

### TypeScript Compilation Errors

**Error:** TypeScript compilation fails

**Solution:**
```bash
cd vscode-extension
npm install
npm run compile
```

## Development

### Watch Mode

For automatic recompilation during development:

```bash
npm run watch
```

### Debugging

1. Open the `vscode-extension` folder in VS Code
2. Go to Run and Debug view (`Ctrl+Shift+D` / `Cmd+Shift+D`)
3. Select "Run Extension" and press F5
4. Use breakpoints in TypeScript files

## License

MIT

## Support

For issues and feature requests, please visit:
https://github.com/jcracelis/vacation_agent/issues
