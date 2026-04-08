# Agents Repository 🤖

A collection of AI-powered agents for various purposes.

## Available Agents

### 🌴 Vacation Agent

An AI-powered vacation planning agent specializing in **adult-only vacations** with verified information from trusted sources.

**Features:**
- Verified destination recommendations from TripAdvisor
- Custom itineraries for adult travelers
- Non-stop flights and rail transportation only
- Accurate budget estimates from approved sources
- Interactive VS Code extension

📖 **[View Vacation Agent Documentation →](agents/README.md)**

**Quick Start:**
```bash
cd agents
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**VS Code Extension:**
```bash
cd vscode-extension
npm install
npm run compile
# Open in VS Code and press F5
```

## Adding New Agents

To add a new agent:

1. Create a new folder in `agents/` with the agent name
2. Follow the standard structure:
   ```
   agents/
   └── agent_name/
       ├── src/
       ├── tests/
       ├── config/
       ├── requirements.txt
       └── README.md
   ```
3. Update this root README.md

## License

MIT
