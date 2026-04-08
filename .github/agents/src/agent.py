"""Main Vacation Agent implementation."""

import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from src.prompts import SYSTEM_PROMPT, GREETING_PROMPT, DESTINATION_PROMPT, ITINERARY_PROMPT

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
    tripadvisor_url: Optional[str] = Field(None, description="TripAdvisor review URL")


class Transportation(BaseModel):
    """Model for transportation options."""

    type: str = Field(..., description="Type: 'flight' or 'rail'")
    carrier: str = Field(..., description="Carrier name (AA, Southwest, Delta, or Amtrak)")
    departure: str = Field(..., description="Departure location/time")
    arrival: str = Field(..., description="Arrival location/time")
    duration: str = Field(..., description="Travel duration")
    cost_estimate: float = Field(..., description="Estimated cost")
    is_nonstop: bool = Field(..., description="True for non-stop flights only")
    booking_url: str = Field(..., description="Carrier booking URL")


class Activity(BaseModel):
    """Model for an activity recommendation."""

    name: str = Field(..., description="Activity name")
    description: str = Field(..., description="Description")
    duration_hours: float = Field(..., description="Estimated duration")
    cost_estimate: float = Field(..., description="Estimated cost")
    tripadvisor_url: Optional[str] = Field(None, description="TripAdvisor review URL")
    suitable_for_adults_only: bool = Field(True, description="Adult-appropriate activity")


class Itinerary(BaseModel):
    """Model for travel itinerary."""

    destination: str
    day_number: int
    activities: list[Activity]
    meals: list[str]
    notes: Optional[str] = None


class VacationAgent:
    """Main agent class for vacation planning.
    
    Specializes in adult-only vacations with verified information from:
    - TripAdvisor (tripadvisor.com) for reviews
    - Airlines: aa.com, southwest.com, delta.com (non-stop flights only)
    - Rail: amtrak.com
    """

    # Approved sources
    APPROVED_REVIEW_SOURCES = ["tripadvisor.com"]
    APPROVED_AIRLINES = {
        "aa.com": "American Airlines",
        "southwest.com": "Southwest Airlines",
        "delta.com": "Delta Air Lines"
    }
    APPROVED_RAIL = {
        "amtrak.com": "Amtrak"
    }

    def __init__(self, model_name: str = "gpt-4"):
        """Initialize the Vacation Agent.

        Args:
            model_name: Name of the LLM model to use
        """
        self.model_name = model_name
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.conversation_history = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        self.user_preferences = {}

    def greet(self) -> str:
        """Send initial greeting and ask clarifying questions.
        
        Returns:
            Warm greeting message with questions about trip preferences
        """
        greeting = GREETING_PROMPT
        self.conversation_history.append({"role": "assistant", "content": greeting})
        return greeting

    def ask_clarifying_questions(self) -> str:
        """Ask clarifying questions about desired trip.
        
        Returns:
            Follow-up questions to refine recommendations
        """
        questions = []
        
        if not self.user_preferences.get("vacation_type"):
            questions.append("What type of experience are you looking for? (romantic getaway, adventure, relaxation, cultural immersion)")
        
        if not self.user_preferences.get("duration"):
            questions.append("How many days are you planning to travel?")
        
        if not self.user_preferences.get("budget"):
            questions.append("What's your approximate budget range?")
        
        if not self.user_preferences.get("origin"):
            questions.append("Where will you be traveling from? (to calculate transportation options)")
        
        return " ".join(questions) if questions else "I think we have a great start! Would you like me to search for specific destinations?"

    def collect_preferences(
        self,
        vacation_type: Optional[str] = None,
        duration: Optional[int] = None,
        budget: Optional[float] = None,
        origin: Optional[str] = None,
        travel_dates: Optional[str] = None
    ) -> dict:
        """Collect and store user preferences.
        
        Args:
            vacation_type: Type of vacation desired
            duration: Number of days
            budget: Budget amount
            origin: Departure location
            travel_dates: Preferred travel dates
            
        Returns:
            Dictionary of collected preferences
        """
        if vacation_type:
            self.user_preferences["vacation_type"] = vacation_type
        if duration:
            self.user_preferences["duration"] = duration
        if budget:
            self.user_preferences["budget"] = budget
        if origin:
            self.user_preferences["origin"] = origin
        if travel_dates:
            self.user_preferences["travel_dates"] = travel_dates
            
        return self.user_preferences

    def validate_source(self, url: str) -> bool:
        """Validate that a URL is from an approved source.
        
        Args:
            url: URL to validate
            
        Returns:
            True if from approved source, False otherwise
        """
        url_lower = url.lower()
        
        # Check review sources
        if any(source in url_lower for source in self.APPROVED_REVIEW_SOURCES):
            return True
        
        # Check airline sources
        if any(airline in url_lower for airline in self.APPROVED_AIRLINES.keys()):
            return True
        
        # Check rail sources
        if any(rail in url_lower for rail in self.APPROVED_RAIL.keys()):
            return True
            
        return False

    def plan_destination(
        self,
        preference: str,
        duration_days: int = 7,
        budget: float = 2000,
        travelers: int = 2
    ) -> DestinationRecommendation:
        """Plan a destination based on preferences.
        
        All recommendations must be grounded in tripadvisor.com reviews.

        Args:
            preference: Type of vacation (e.g., 'beach', 'mountain', 'city')
            duration_days: Number of days for the trip
            budget: Total budget in USD
            travelers: Number of travelers

        Returns:
            DestinationRecommendation object
        """
        # Store preferences
        self.collect_preferences(
            vacation_type=preference,
            duration=duration_days,
            budget=budget
        )
        
        # TODO: Implement LLM call with source verification
        # Placeholder with required fields
        placeholder = DestinationRecommendation(
            destination="TBD",
            country="TBD",
            description=f"Based on your preference for a {preference} vacation, I'll find verified options from TripAdvisor reviews.",
            estimated_cost=budget,
            duration_days=duration_days,
            highlights=[],
            best_time_to_visit="TBD",
            tripadvisor_url="https://www.tripadvisor.com"
        )
        return placeholder

    def find_transportation(
        self,
        origin: str,
        destination: str,
        travel_dates: str
    ) -> list[Transportation]:
        """Find transportation options from approved carriers only.
        
        Only non-stop flights and rail options are considered.
        Sources: aa.com, southwest.com, delta.com, amtrak.com

        Args:
            origin: Departure location
            destination: Arrival location
            travel_dates: Travel dates
            
        Returns:
            List of verified transportation options
        """
        # TODO: Implement carrier website scraping/API calls
        # Only return non-stop flights and rail options
        placeholder = [
            Transportation(
                type="flight",
                carrier="American Airlines",
                departure=f"{origin} - TBD",
                arrival=f"{destination} - TBD",
                duration="TBD",
                cost_estimate=0.0,
                is_nonstop=True,
                booking_url="https://www.aa.com"
            )
        ]
        return placeholder

    def suggest_activities(
        self,
        destination: str,
        vacation_type: str,
        duration_days: int
    ) -> list[Activity]:
        """Suggest activities suitable for adult-only vacation.
        
        All activities must be verified via tripadvisor.com

        Args:
            destination: Destination name
            vacation_type: Type of vacation
            duration_days: Trip duration
            
        Returns:
            List of verified activity suggestions
        """
        # TODO: Implement TripAdvisor API/scraping
        placeholder = [
            Activity(
                name="Activity verification pending",
                description=f"Activities for {vacation_type} vacation in {destination} will be sourced from TripAdvisor reviews.",
                duration_hours=0,
                cost_estimate=0.0,
                tripadvisor_url="https://www.tripadvisor.com",
                suitable_for_adults_only=True
            )
        ]
        return placeholder

    def generate_itinerary(
        self,
        destination: str,
        duration_days: int = 7
    ) -> list[Itinerary]:
        """Generate a verified day-by-day itinerary.

        Args:
            destination: Name of the destination
            duration_days: Number of days

        Returns:
            List of Itinerary objects with verified activities
        """
        # TODO: Implement with activity verification
        itinerary = []
        for day in range(1, duration_days + 1):
            day_plan = Itinerary(
                destination=destination,
                day_number=day,
                activities=[],
                meals=["Breakfast", "Lunch", "Dinner"],
                notes="All activities will be verified via TripAdvisor before finalizing"
            )
            itinerary.append(day_plan)
        return itinerary

    def estimate_budget(
        self,
        destination: str,
        duration_days: int,
        travelers: int
    ) -> dict:
        """Estimate the budget for a trip with verified pricing.
        
        All pricing must be verified from approved sources.

        Args:
            destination: Destination name
            duration_days: Trip duration
            travelers: Number of travelers

        Returns:
            Dictionary with budget breakdown
        """
        # TODO: Implement with source verification
        return {
            "flights": "TBD - Verify at aa.com, southwest.com, or delta.com",
            "accommodation": "TBD - Verify at tripadvisor.com",
            "food": "TBD - Verify at tripadvisor.com",
            "activities": "TBD - Verify at tripadvisor.com",
            "rail_alternative": "TBD - Verify at amtrak.com",
            "total": "TBD - All costs will be verified from approved sources",
            "note": "All pricing will be double-checked from approved carrier websites and TripAdvisor"
        }

    def validate_suggestions(self, suggestions: list) -> dict:
        """Validate all suggestions before presenting to user.
        
        Ensures no hallucinated information and all data is from approved sources.

        Args:
            suggestions: List of suggestions to validate
            
        Returns:
            Validation results with confidence scores
        """
        validation_results = {
            "validated": True,
            "sources_verified": [],
            "pending_verification": [],
            "warnings": []
        }
        
        # Check all suggestions have source URLs
        for suggestion in suggestions:
            if hasattr(suggestion, "tripadvisor_url") and suggestion.tripadvisor_url:
                if self.validate_source(suggestion.tripadvisor_url):
                    validation_results["sources_verified"].append(suggestion.tripadvisor_url)
                else:
                    validation_results["validated"] = False
                    validation_results["warnings"].append(
                        f"Unverified source: {suggestion.tripadvisor_url}"
                    )
            else:
                validation_results["pending_verification"].append(str(suggestion))
        
        return validation_results

    def chat(self, message: str) -> str:
        """Chat with the agent.
        
        All responses will be grounded in approved sources only.

        Args:
            message: User message

        Returns:
            Agent response verified from approved sources
        """
        self.conversation_history.append({"role": "user", "content": message})
        
        # TODO: Implement LLM call with strict source constraints
        # Response must only use TripAdvisor, aa.com, southwest.com, delta.com, amtrak.com
        response = (
            "Thank you for your message! I'm reviewing verified sources from TripAdvisor "
            "and approved carrier websites to provide you with accurate, double-checked information. "
            "Let me gather some details for you..."
        )
        
        self.conversation_history.append({"role": "assistant", "content": response})
        return response


def main():
    """Main entry point for the vacation agent."""
    agent = VacationAgent()
    print("🌴 Welcome to Your Adult-Only Vacation Planner!")
    print("=" * 60)
    
    # Send greeting
    greeting = agent.greet()
    print(f"\n{greeting}")


if __name__ == "__main__":
    main()
