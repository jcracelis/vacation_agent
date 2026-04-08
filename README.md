# Vacation Agent 🌴

An AI-powered vacation planning agent specializing in **adult-only vacations** with verified information from trusted sources.

## Key Features

- 🌍 **Verified Destination Recommendations** - All suggestions grounded in TripAdvisor reviews
- 📅 **Custom Itineraries** - Personalized day-by-day plans for adult travelers
- ✈️ **Verified Transportation** - Non-stop flights (aa.com, southwest.com, delta.com) and rail (amtrak.com) only
- 💰 **Accurate Budget Estimates** - All pricing double-checked from approved sources
- 🔍 **Source Validation** - No hallucination; all information validated before presentation
- 💬 **Warm, Personal Service** - Clarifying questions to understand your preferences

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

## Development

```bash
# Run tests
pytest tests/

# Run linting
flake8 src/
```

## License

MIT
