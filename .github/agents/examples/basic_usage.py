"""Example usage of Vacation Agent - Adult Only Vacation Planner."""

from src.agent import VacationAgent


def main():
    """Demonstrate Vacation Agent capabilities."""
    # Initialize the agent
    agent = VacationAgent()
    
    # Example 1: Send greeting and ask clarifying questions
    print("🌴 Welcome to Your Adult-Only Vacation Planner!")
    print("=" * 60)
    greeting = agent.greet()
    print(f"\n{greeting}\n")
    
    # Example 2: Collect preferences
    print("📝 Collecting Preferences...")
    print("=" * 60)
    preferences = agent.collect_preferences(
        vacation_type="romantic beach getaway",
        duration=7,
        budget=3500,
        origin="Chicago, IL",
        travel_dates="May 15-22, 2026"
    )
    print(f"Recorded preferences: {preferences}\n")
    
    # Example 3: Ask follow-up questions
    print("❓ Follow-up Questions...")
    print("=" * 60)
    questions = agent.ask_clarifying_questions()
    print(f"{questions}\n")
    
    # Example 4: Plan destination (verified via TripAdvisor)
    print("🏖️  Planning Destination...")
    print("=" * 60)
    destination = agent.plan_destination(
        preference="romantic beach",
        duration_days=7,
        budget=3500,
        travelers=2
    )
    print(f"Destination: {destination.destination}, {destination.country}")
    print(f"Estimated Cost: ${destination.estimated_cost:,.2f}")
    print(f"Verified Source: {destination.tripadvisor_url}\n")
    
    # Example 5: Find transportation (non-stop only)
    print("✈️  Finding Transportation...")
    print("=" * 60)
    transport_options = agent.find_transportation(
        origin="Chicago, IL",
        destination="Cancun, Mexico",
        travel_dates="2026-05-15"
    )
    for option in transport_options:
        print(f"{option.type.capitalize()} via {option.carrier}")
        print(f"  Non-stop: {option.is_nonstop}")
        print(f"  Booking: {option.booking_url}\n")
    
    # Example 6: Validate all suggestions
    print("🔍 Validating Suggestions...")
    print("=" * 60)
    validation = agent.validate_suggestions([destination])
    print(f"Validation Status: {'✓ Verified' if validation['validated'] else '✗ Pending'}")
    print(f"Sources Verified: {len(validation['sources_verified'])}")
    if validation['warnings']:
        print(f"Warnings: {validation['warnings']}")
    print()
    
    # Example 7: Interactive chat
    print("💬 Chat Example")
    print("=" * 60)
    response = agent.chat("What are some romantic activities in Cancun?")
    print(response)


if __name__ == "__main__":
    main()
