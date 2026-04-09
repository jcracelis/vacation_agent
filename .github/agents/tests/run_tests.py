"""Quick import test for the Vacation Agent."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from src.agent import VacationAgent, LLM_PROVIDERS, _detect_provider
    from src.models import Traveler, TripDetails, TravelStyle
    from src.utils import format_currency, split_budget

    print("  Imports:          OK")
    print(f"  Providers:        {', '.join(LLM_PROVIDERS.keys())}")
    print(f"  Auto-detect:      {_detect_provider()}")

    agent = VacationAgent()
    print(f"  Active provider:  {agent.provider}")
    print(f"  Model:            {agent.model_name}")
    print(f"  LLM available:    {agent.is_llm_available()}")
    print(f"  Base URL:         {agent.get_base_url()}")

    # Test core methods
    greeting = agent.greet()
    assert len(greeting) > 50
    print(f"  Greeting:         OK ({len(greeting)} chars)")

    prefs = agent.collect_preferences(
        vacation_type="beach", duration=7, budget=3000
    )
    assert prefs["vacation_type"] == "beach"
    print(f"  Preferences:      OK")

    result = agent.plan_destination("beach", 7, 3000)
    assert result.destination is not None
    print(f"  Plan destination: OK ({result.destination})")

    transport = agent.find_transportation("Chicago", "Miami", "2026-05-15")
    assert len(transport) > 0
    assert transport[0].is_nonstop is True
    print(f"  Transportation:   OK ({transport[0].carrier})")

    activities = agent.suggest_activities("Cancun", "beach", 7)
    assert len(activities) > 0
    print(f"  Activities:       OK ({len(activities)})")

    itinerary = agent.generate_itinerary("Cancun", 7)
    assert len(itinerary) == 7
    print(f"  Itinerary:        OK ({len(itinerary)} days)")

    budget = agent.estimate_budget("Cancun", 7, 2)
    assert "total" in budget
    print(f"  Budget estimate:  OK")

    response = agent.chat("Hello!")
    assert len(response) > 20
    print(f"  Chat response:    OK ({len(response)} chars)")

    validation = agent.validate_suggestions([result])
    print(f"  Source validation: OK (verified: {len(validation['sources_verified'])})")

    print()
    print("  ALL CHECKS PASSED!")

except Exception as e:
    print(f"  FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
