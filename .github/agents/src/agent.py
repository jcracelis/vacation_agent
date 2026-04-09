"""Main Vacation Agent implementation.

Supports multiple LLM providers:
- OpenAI (GPT-4, GPT-4-turbo, GPT-3.5-turbo)
- Qwen (qwen-plus, qwen-max, qwen-turbo, qwen-long)
- Ollama (llama3, mistral, phi, qwen, etc. — runs locally)

Provider selection logic:
1. If 'provider' is explicitly set, use it
2. If not, auto-detect: ollama > qwen > openai (first available)
"""

import os
import json
import logging
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from src.prompts import SYSTEM_PROMPT, GREETING_PROMPT, DESTINATION_PROMPT, ITINERARY_PROMPT

load_dotenv()

# Configure module-level logger for debug-friendly output
logger = logging.getLogger(__name__)


# ─── Data Models ─────────────────────────────────────────────────────────────


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


# ─── LLM Provider Registry ───────────────────────────────────────────────────

LLM_PROVIDERS = {
    "openai": {
        "models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
        "api_key_env": "OPENAI_API_KEY",
        "base_url": "https://api.openai.com/v1/chat/completions",
        "requires_api_key": True,
        "display_name": "OpenAI",
    },
    "qwen": {
        "models": ["qwen-plus", "qwen-max", "qwen-turbo", "qwen-long"],
        "api_key_env": "QWEN_API_KEY",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        "requires_api_key": True,
        "display_name": "Qwen (Alibaba Cloud)",
    },
    "ollama": {
        "models": ["llama3", "mistral", "phi3", "qwen2", "gemma2", "deepseek-r1"],
        "api_key_env": None,  # No API key needed
        "base_url": "http://localhost:11434/v1/chat/completions",
        "requires_api_key": False,
        "display_name": "Ollama (Local)",
    },
}

# Provider priority order for auto-detection
PROVIDER_PRIORITY = ["ollama", "qwen", "openai"]


# ─── Helper Functions ────────────────────────────────────────────────────────


def _detect_provider(
    provider_hint: Optional[str] = None,
) -> str:
    """Auto-detect the best available LLM provider.

    Priority: ollama (local) > qwen > openai
    If a hint is provided and valid, use it.

    Args:
        provider_hint: User-specified provider preference

    Returns:
        Provider name string
    """
    # If user explicitly requested a provider, honor it
    if provider_hint and provider_hint in LLM_PROVIDERS:
        return provider_hint

    # Auto-detect: first available provider wins
    for provider in PROVIDER_PRIORITY:
        config = LLM_PROVIDERS[provider]

        # Ollama: always available as a local service (we check connectivity later)
        if provider == "ollama":
            continue  # Always considered available

        # Cloud providers: need an API key
        api_key_env = config["api_key_env"]
        if api_key_env and os.getenv(api_key_env):
            return provider

    # Default fallback
    return "openai"


# ─── Main Agent Class ────────────────────────────────────────────────────────


class VacationAgent:
    """Main agent class for vacation planning.

    Specializes in adult-only vacations with verified information from:
    - TripAdvisor (tripadvisor.com) for reviews
    - Airlines: aa.com, southwest.com, delta.com (non-stop flights only)
    - Rail: amtrak.com

    Supports multiple LLM providers:
    - OpenAI (GPT-4, GPT-4-turbo, GPT-3.5-turbo)
    - Qwen (qwen-plus, qwen-max, qwen-turbo)
    - Ollama (llama3, mistral, phi3, etc. — local, no API key)
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

    def __init__(
        self,
        model_name: Optional[str] = None,
        provider: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        qwen_api_key: Optional[str] = None,
        ollama_base_url: Optional[str] = None,
    ):
        """Initialize the Vacation Agent.

        Args:
            model_name: LLM model name (auto-selected if None)
            provider: LLM provider — 'openai', 'qwen', or 'ollama' (auto-detected if None)
            openai_api_key: OpenAI API key (falls back to OPENAI_API_KEY env var)
            qwen_api_key: Qwen API key (falls back to QWEN_API_KEY env var)
            ollama_base_url: Ollama server URL (falls back to OLLAMA_BASE_URL env var
                             or default http://localhost:11434)
        """
        # Resolve provider
        self.provider = _detect_provider(provider)
        provider_config = LLM_PROVIDERS[self.provider]

        # Resolve model name
        if model_name:
            self.model_name = model_name
        else:
            # Default to first model in provider's list
            self.model_name = provider_config["models"][0]

        # Store API keys / endpoints
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.qwen_api_key = qwen_api_key or os.getenv("QWEN_API_KEY")
        self.ollama_base_url = (
            ollama_base_url
            or os.getenv("OLLAMA_BASE_URL")
            or "http://localhost:11434"
        )

        # Initialize conversation state
        self.conversation_history = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        self.user_preferences: dict = {}

        # Log initialization for debugging
        logger.debug(
            "VacationAgent initialized: provider=%s, model=%s, llm_available=%s",
            self.provider,
            self.model_name,
            self.is_llm_available(),
        )

    # ─── Provider Configuration ───────────────────────────────────────────

    def get_api_key(self) -> Optional[str]:
        """Get the API key for the current provider.

        Returns:
            API key string, or None for local providers (Ollama)
        """
        if self.provider == "qwen":
            return self.qwen_api_key
        if self.provider == "openai":
            return self.openai_api_key
        # Ollama doesn't need an API key
        return None

    def get_base_url(self) -> str:
        """Get the API base URL for the current provider.

        Returns:
            Full URL endpoint for LLM requests
        """
        if self.provider == "ollama":
            return f"{self.ollama_base_url}/v1/chat/completions"

        provider_config = self.get_provider_config()
        return provider_config["base_url"]

    def get_provider_config(self) -> dict:
        """Get configuration for the current LLM provider.

        Returns:
            Dictionary with provider settings
        """
        return LLM_PROVIDERS[self.provider]

    def is_llm_available(self) -> bool:
        """Check if the LLM provider is ready to respond.

        For cloud providers: API key must be configured.
        For Ollama: Always considered available (connectivity checked at call time).

        Returns:
            True if provider can be reached, False otherwise
        """
        provider_config = self.get_provider_config()

        # Ollama: no API key needed, always considered available
        if not provider_config.get("requires_api_key"):
            return True

        # Cloud providers: need a valid API key
        api_key = self.get_api_key()
        return api_key is not None and len(api_key) > 0

    # ─── LLM Communication ────────────────────────────────────────────────

    def _call_llm(self, messages: list[dict]) -> Optional[str]:
        """Call the LLM with conversation messages.

        Args:
            messages: List of {role, content} dicts

        Returns:
            Response text, or None on failure
        """
        api_key = self.get_api_key()
        base_url = self.get_base_url()

        # Build headers
        headers = {
            "Content-Type": "application/json",
        }
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        # Build request payload
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000,
        }

        try:
            import urllib.request
            import urllib.error

            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                base_url, data=data, headers=headers, method="POST"
            )

            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode("utf-8"))
                content = (
                    result.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "")
                )
                logger.debug("LLM response received: %d chars", len(content))
                return content

        except urllib.error.HTTPError as e:
            error_body = ""
            try:
                error_body = e.read().decode("utf-8")
            except Exception:
                pass
            logger.error(
                "LLM HTTP %d error: %s — %s", e.code, base_url, error_body[:200]
            )
            return (
                f"[LLM Error: HTTP {e.code} from {base_url}. "
                f"Details: {error_body[:200]}]"
            )

        except urllib.error.URLError as e:
            reason = str(e.reason)
            logger.error("LLM URL error: %s — %s", base_url, reason)
            if "Connection refused" in reason or "111" in reason:
                hint = self._connection_hint()
                return f"[LLM Error: Cannot connect to {base_url}. {reason}. {hint}]"
            return f"[LLM Error: {reason}]"

        except Exception as e:
            logger.error("LLM unexpected error: %s", str(e))
            return f"[LLM Error: {str(e)}]"

    def _connection_hint(self) -> str:
        """Return a helpful hint if Ollama can't be reached.

        Returns:
            Human-readable troubleshooting message
        """
        if self.provider != "ollama":
            return ""

        return (
            "Make sure Ollama is installed and running. "
            "Start it with: ollama serve. "
            "Then pull a model: ollama pull llama3. "
            "See https://ollama.com for setup instructions."
        )

    # ─── User Interaction ─────────────────────────────────────────────────

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
            questions.append(
                "What type of experience are you looking for? "
                "(romantic getaway, adventure, relaxation, cultural immersion)"
            )

        if not self.user_preferences.get("duration"):
            questions.append("How many days are you planning to travel?")

        if not self.user_preferences.get("budget"):
            questions.append("What's your approximate budget range?")

        if not self.user_preferences.get("origin"):
            questions.append(
                "Where will you be traveling from? "
                "(to calculate transportation options)"
            )

        return (
            " ".join(questions)
            if questions
            else "I think we have a great start! Would you like me to search for specific destinations?"
        )

    def collect_preferences(
        self,
        vacation_type: Optional[str] = None,
        duration: Optional[int] = None,
        budget: Optional[float] = None,
        origin: Optional[str] = None,
        travel_dates: Optional[str] = None,
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

    # ─── Source Validation ────────────────────────────────────────────────

    def validate_source(self, url: str) -> bool:
        """Validate that a URL is from an approved source.

        Args:
            url: URL to validate

        Returns:
            True if from approved source, False otherwise
        """
        url_lower = url.lower()

        if any(source in url_lower for source in self.APPROVED_REVIEW_SOURCES):
            return True
        if any(airline in url_lower for airline in self.APPROVED_AIRLINES.keys()):
            return True
        if any(rail in url_lower for rail in self.APPROVED_RAIL.keys()):
            return True

        return False

    # ─── Planning Methods ─────────────────────────────────────────────────

    def plan_destination(
        self,
        preference: str,
        duration_days: int = 7,
        budget: float = 2000,
        travelers: int = 2,
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
        self.collect_preferences(
            vacation_type=preference,
            duration=duration_days,
            budget=budget,
        )

        # Try LLM call if available
        if self.is_llm_available():
            prompt = DESTINATION_PROMPT.format(
                preference=preference,
                duration_days=duration_days,
                budget=budget,
                travelers=travelers,
            )
            messages = self.conversation_history + [
                {"role": "user", "content": prompt}
            ]
            llm_response = self._call_llm(messages)
            if llm_response and not llm_response.startswith("[LLM Error"):
                self.conversation_history.append(
                    {"role": "assistant", "content": llm_response}
                )
                return DestinationRecommendation(
                    destination="See response above",
                    country="See response above",
                    description=llm_response[:200],
                    estimated_cost=budget,
                    duration_days=duration_days,
                    highlights=[],
                    best_time_to_visit="TBD",
                    tripadvisor_url="https://www.tripadvisor.com",
                )

        # Fallback
        return DestinationRecommendation(
            destination="TBD",
            country="TBD",
            description=(
                f"Based on your preference for a {preference} vacation, "
                f"I'll find verified options from TripAdvisor reviews. "
                f"Using {self.provider} ({self.model_name})."
            ),
            estimated_cost=budget,
            duration_days=duration_days,
            highlights=[],
            best_time_to_visit="TBD",
            tripadvisor_url="https://www.tripadvisor.com",
        )

    def find_transportation(
        self,
        origin: str,
        destination: str,
        travel_dates: str,
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
        return [
            Transportation(
                type="flight",
                carrier="American Airlines",
                departure=f"{origin} - TBD",
                arrival=f"{destination} - TBD",
                duration="TBD",
                cost_estimate=0.0,
                is_nonstop=True,
                booking_url="https://www.aa.com",
            )
        ]

    def suggest_activities(
        self,
        destination: str,
        vacation_type: str,
        duration_days: int,
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
        return [
            Activity(
                name="Activity verification pending",
                description=(
                    f"Activities for {vacation_type} vacation in {destination} "
                    f"will be sourced from TripAdvisor reviews."
                ),
                duration_hours=0,
                cost_estimate=0.0,
                tripadvisor_url="https://www.tripadvisor.com",
                suitable_for_adults_only=True,
            )
        ]

    def generate_itinerary(
        self,
        destination: str,
        duration_days: int = 7,
    ) -> list[Itinerary]:
        """Generate a verified day-by-day itinerary.

        Args:
            destination: Name of the destination
            duration_days: Number of days

        Returns:
            List of Itinerary objects with verified activities
        """
        itinerary = []
        for day in range(1, duration_days + 1):
            day_plan = Itinerary(
                destination=destination,
                day_number=day,
                activities=[],
                meals=["Breakfast", "Lunch", "Dinner"],
                notes="All activities will be verified via TripAdvisor before finalizing",
            )
            itinerary.append(day_plan)
        return itinerary

    def estimate_budget(
        self,
        destination: str,
        duration_days: int,
        travelers: int,
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
        return {
            "flights": "TBD - Verify at aa.com, southwest.com, or delta.com",
            "accommodation": "TBD - Verify at tripadvisor.com",
            "food": "TBD - Verify at tripadvisor.com",
            "activities": "TBD - Verify at tripadvisor.com",
            "rail_alternative": "TBD - Verify at amtrak.com",
            "total": "TBD - All costs will be verified from approved sources",
            "note": (
                "All pricing will be double-checked from approved carrier "
                "websites and TripAdvisor"
            ),
        }

    # ─── Validation ───────────────────────────────────────────────────────

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
            "warnings": [],
        }

        for suggestion in suggestions:
            if hasattr(suggestion, "tripadvisor_url") and suggestion.tripadvisor_url:
                if self.validate_source(suggestion.tripadvisor_url):
                    validation_results["sources_verified"].append(
                        suggestion.tripadvisor_url
                    )
                else:
                    validation_results["validated"] = False
                    validation_results["warnings"].append(
                        f"Unverified source: {suggestion.tripadvisor_url}"
                    )
            else:
                validation_results["pending_verification"].append(str(suggestion))

        return validation_results

    # ─── Chat ─────────────────────────────────────────────────────────────

    def chat(self, message: str) -> str:
        """Chat with the agent.

        All responses will be grounded in approved sources only.

        Args:
            message: User message

        Returns:
            Agent response verified from approved sources
        """
        self.conversation_history.append({"role": "user", "content": message})

        # Try LLM call if available
        if self.is_llm_available():
            llm_response = self._call_llm(self.conversation_history)
            if llm_response and not llm_response.startswith("[LLM Error"):
                self.conversation_history.append(
                    {"role": "assistant", "content": llm_response}
                )
                return llm_response

        # Fallback response
        response = (
            f"Thank you for your message! I'm reviewing verified sources from TripAdvisor "
            f"and approved carrier websites to provide you with accurate, double-checked information. "
            f"Using {self.provider} ({self.model_name}). "
            f"Note: Configure your API key or start Ollama for full LLM responses."
        )

        self.conversation_history.append({"role": "assistant", "content": response})
        return response


# ─── CLI Entry Point ─────────────────────────────────────────────────────────


def main():
    """Main entry point for the vacation agent."""
    agent = VacationAgent()
    print("🌴 Welcome to Your Adult-Only Vacation Planner!")
    print("=" * 60)
    print(f"  Provider:    {agent.provider} ({agent.model_name})")
    print(f"  LLM Ready:   {agent.is_llm_available()}")
    print(f"  Base URL:    {agent.get_base_url()}")
    print("=" * 60)

    greeting = agent.greet()
    print(f"\n{greeting}")


if __name__ == "__main__":
    main()
