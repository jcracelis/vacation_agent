# Vacation Agent 🌴

An AI-powered vacation planning agent that helps you discover destinations, plan itineraries, and organize your travel details.

## Features

- 🌍 **Destination Discovery** - Find personalized vacation recommendations
- 📅 **Itinerary Planning** - Generate day-by-day travel plans
- 💰 **Budget Estimation** - Get cost estimates for trips
- ✈️ **Travel Assistance** - Helpful tips and information for your journey

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
├── .gitignore
├── requirements.txt        # Python dependencies
├── setup.py                # Package setup
└── README.md
```

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd vacation_agent

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```python
from src.agent import VacationAgent

agent = VacationAgent()
response = agent.plan_destination("beach", 7, 2000)
print(response)
```

## Development

```bash
# Run tests
pytest tests/

# Run linting
flake8 src/
```

## License

MIT
