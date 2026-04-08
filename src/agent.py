"""Main Vacation Agent implementation."""

import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


class DestinationRecommendation(BaseModel):
    """Model for destination recommendations."""
    
    destination: str = Field(..., description="Name of the destination")
    country: str = Field(..., description="Country name")
    description: str = Field(..., description="Brief description")
    estimated_cost: float = Field(..., description="Estimated cost in USD")
    duration_days: int = Field(..., description="Recommended duration in days")
    highlights: list[str] = Field(default_factory=list, description="Top attractions/activities")
    best_time_to_visit: str = Field(..., description="Best season/month to visit")


class Itinerary(BaseModel):
    """Model for travel itinerary."""
    
    destination: str
    day_number: int
    activities: list[str]
    meals: list[str]
    notes: Optional[str] = None


class VacationAgent:
    """Main agent class for vacation planning."""
    
    def __init__(self, model_name: str = "gpt-4"):
        """Initialize the Vacation Agent.
        
        Args:
            model_name: Name of the LLM model to use
        """
        self.model_name = model_name
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.conversation_history = []
        
    def plan_destination(
        self,
        preference: str,
        duration_days: int = 7,
        budget: float = 2000,
        travelers: int = 2
    ) -> DestinationRecommendation:
        """Plan a destination based on preferences.
        
        Args:
            preference: Type of vacation (e.g., 'beach', 'mountain', 'city')
            duration_days: Number of days for the trip
            budget: Total budget in USD
            travelers: Number of travelers
            
        Returns:
            DestinationRecommendation object
        """
        # TODO: Implement LLM call for destination recommendation
        placeholder = DestinationRecommendation(
            destination="Bali",
            country="Indonesia",
            description=f"Beautiful {preference} destination with stunning landscapes",
            estimated_cost=budget * 0.8,
            duration_days=duration_days,
            highlights=["Temple visits", "Beach relaxation", "Local cuisine", "Cultural experiences"],
            best_time_to_visit="April to October"
        )
        return placeholder
    
    def generate_itinerary(
        self,
        destination: str,
        duration_days: int = 7
    ) -> list[Itinerary]:
        """Generate a day-by-day itinerary.
        
        Args:
            destination: Name of the destination
            duration_days: Number of days
            
        Returns:
            List of Itinerary objects
        """
        itinerary = []
        for day in range(1, duration_days + 1):
            day_plan = Itinerary(
                destination=destination,
                day_number=day,
                activities=[f"Activity {day} - To be implemented"],
                meals=["Breakfast", "Lunch", "Dinner"],
                notes="Customize based on preferences"
            )
            itinerary.append(day_plan)
        return itinerary
    
    def estimate_budget(
        self,
        destination: str,
        duration_days: int,
        travelers: int
    ) -> dict:
        """Estimate the budget for a trip.
        
        Args:
            destination: Destination name
            duration_days: Trip duration
            travelers: Number of travelers
            
        Returns:
            Dictionary with budget breakdown
        """
        # TODO: Implement budget estimation
        return {
            "flights": 500 * travelers,
            "accommodation": 100 * duration_days,
            "food": 50 * duration_days * travelers,
            "activities": 100 * duration_days,
            "miscellaneous": 200,
            "total": (500 * travelers) + (100 * duration_days) + (50 * duration_days * travelers) + (100 * duration_days) + 200
        }
    
    def chat(self, message: str) -> str:
        """Chat with the agent.
        
        Args:
            message: User message
            
        Returns:
            Agent response
        """
        # TODO: Implement chat functionality with LLM
        self.conversation_history.append({"role": "user", "content": message})
        response = f"Received: {message}. This is a placeholder response."
        self.conversation_history.append({"role": "assistant", "content": response})
        return response


def main():
    """Main entry point for the vacation agent."""
    agent = VacationAgent()
    print("🌴 Welcome to Vacation Agent!")
    print("=" * 50)
    
    # Example usage
    destination = agent.plan_destination("beach", 7, 2000)
    print(f"\n📍 Recommended: {destination.destination}, {destination.country}")
    print(f"💰 Estimated Cost: ${destination.estimated_cost:.2f}")
    print(f"✨ Highlights: {', '.join(destination.highlights)}")


if __name__ == "__main__":
    main()
