"""Example usage of Vacation Agent."""

from src.agent import VacationAgent
from src.utils import format_currency


def main():
    """Demonstrate Vacation Agent capabilities."""
    # Initialize the agent
    agent = VacationAgent()
    
    # Example 1: Plan a beach vacation
    print("🏖️  Beach Vacation Planning")
    print("=" * 60)
    destination = agent.plan_destination(
        preference="beach",
        duration_days=7,
        budget=2500,
        travelers=2
    )
    print(f"Destination: {destination.destination}, {destination.country}")
    print(f"Estimated Cost: {format_currency(destination.estimated_cost)}")
    print(f"Duration: {destination.duration_days} days")
    print(f"Best Time to Visit: {destination.best_time_to_visit}")
    print(f"Highlights: {', '.join(destination.highlights)}")
    print()
    
    # Example 2: Generate itinerary
    print("📅 Sample Itinerary")
    print("=" * 60)
    itinerary = agent.generate_itinerary(destination.destination, 3)
    for day in itinerary:
        print(f"\nDay {day.day_number}:")
        for activity in day.activities:
            print(f"  • {activity}")
    print()
    
    # Example 3: Budget breakdown
    print("💰 Budget Breakdown")
    print("=" * 60)
    budget = agent.estimate_budget(
        destination=destination.destination,
        duration_days=7,
        travelers=2
    )
    for category, amount in budget.items():
        print(f"{category.capitalize()}: {format_currency(amount)}")
    print()
    
    # Example 4: Interactive chat
    print("💬 Chat Example")
    print("=" * 60)
    response = agent.chat("What are some good activities in Bali?")
    print(response)


if __name__ == "__main__":
    main()
