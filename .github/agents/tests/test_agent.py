"""Tests for the Vacation Agent."""

import pytest
from src.agent import VacationAgent, DestinationRecommendation, Transportation, Activity, LLM_PROVIDERS
from src.models import Traveler, TripDetails, TravelStyle
from src.utils import load_config, format_currency, split_budget


class TestVacationAgent:
    """Test cases for VacationAgent class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.agent = VacationAgent()

    def test_init(self):
        """Test agent initialization."""
        assert self.agent.model_name == "gpt-4"
        assert self.agent.provider == "openai"
        assert len(self.agent.conversation_history) == 1  # System prompt
        assert self.agent.conversation_history[0]["role"] == "system"
        assert self.agent.user_preferences == {}
        assert "tripadvisor.com" in self.agent.APPROVED_REVIEW_SOURCES
        assert "aa.com" in self.agent.APPROVED_AIRLINES

    def test_init_qwen_provider(self):
        """Test agent initialization with Qwen provider."""
        agent = VacationAgent(provider="qwen", model_name="qwen-plus")
        assert agent.provider == "qwen"
        assert agent.model_name == "qwen-plus"

    def test_llm_providers_config(self):
        """Test that LLM providers are properly configured."""
        assert "openai" in LLM_PROVIDERS
        assert "qwen" in LLM_PROVIDERS
        assert LLM_PROVIDERS["openai"]["base_url"] is not None
        assert LLM_PROVIDERS["qwen"]["base_url"] is not None
        assert len(LLM_PROVIDERS["openai"]["models"]) > 0
        assert len(LLM_PROVIDERS["qwen"]["models"]) > 0

    def test_get_api_key_openai(self):
        """Test getting OpenAI API key."""
        agent = VacationAgent(openai_api_key="test-key")
        assert agent.get_api_key() == "test-key"

    def test_get_api_key_qwen(self):
        """Test getting Qwen API key."""
        agent = VacationAgent(provider="qwen", qwen_api_key="test-qwen-key")
        assert agent.get_api_key() == "test-qwen-key"

    def test_get_provider_config(self):
        """Test getting provider configuration."""
        agent = VacationAgent()
        config = agent.get_provider_config()
        assert "base_url" in config
        assert "models" in config
        assert "api_key_env" in config

    def test_is_llm_available_no_key(self):
        """Test LLM availability without API key."""
        agent = VacationAgent()
        # Should be False when no key is provided
        assert agent.is_llm_available() == False

    def test_is_llm_available_with_key(self):
        """Test LLM availability with API key."""
        agent = VacationAgent(openai_api_key="sk-test-key")
        assert agent.is_llm_available() == True

    def test_greet(self):
        """Test greeting functionality."""
        greeting = self.agent.greet()
        assert isinstance(greeting, str)
        assert len(greeting) > 0
        assert len(self.agent.conversation_history) == 2  # System + greeting

    def test_ask_clarifying_questions(self):
        """Test clarifying questions."""
        questions = self.agent.ask_clarifying_questions()
        assert isinstance(questions, str)
        assert len(questions) > 0

    def test_collect_preferences(self):
        """Test preference collection."""
        prefs = self.agent.collect_preferences(
            vacation_type="beach",
            duration=7,
            budget=3000,
            origin="Chicago",
            travel_dates="May 2026"
        )
        assert prefs["vacation_type"] == "beach"
        assert prefs["duration"] == 7
        assert prefs["budget"] == 3000
        assert prefs["origin"] == "Chicago"
        assert prefs["travel_dates"] == "May 2026"

    def test_validate_source_approved(self):
        """Test source validation for approved sources."""
        assert self.agent.validate_source("https://www.tripadvisor.com/Attraction_Review") == True
        assert self.agent.validate_source("https://www.aa.com/flights") == True
        assert self.agent.validate_source("https://www.southwest.com") == True
        assert self.agent.validate_source("https://www.delta.com") == True
        assert self.agent.validate_source("https://www.amtrak.com") == True

    def test_validate_source_unapproved(self):
        """Test source validation rejects unapproved sources."""
        assert self.agent.validate_source("https://www.expedia.com") == False
        assert self.agent.validate_source("https://www.booking.com") == False
        assert self.agent.validate_source("https://www.yelp.com") == False

    def test_plan_destination(self):
        """Test destination planning."""
        result = self.agent.plan_destination("beach", 7, 3000)
        assert isinstance(result, DestinationRecommendation)
        assert result.tripadvisor_url is not None
        assert self.agent.validate_source(result.tripadvisor_url) == True

    def test_find_transportation(self):
        """Test transportation finding."""
        transport = self.agent.find_transportation("Chicago", "Miami", "2026-05-15")
        assert len(transport) > 0
        assert isinstance(transport[0], Transportation)
        assert transport[0].is_nonstop == True
        assert self.agent.validate_source(transport[0].booking_url) == True

    def test_suggest_activities(self):
        """Test activity suggestions."""
        activities = self.agent.suggest_activities("Cancun", "beach", 7)
        assert len(activities) > 0
        assert isinstance(activities[0], Activity)
        assert activities[0].suitable_for_adults_only == True

    def test_generate_itinerary(self):
        """Test itinerary generation."""
        itinerary = self.agent.generate_itinerary("Cancun", 7)
        assert len(itinerary) == 7
        assert all(day.day_number == i+1 for i, day in enumerate(itinerary))

    def test_estimate_budget(self):
        """Test budget estimation."""
        budget = self.agent.estimate_budget("Cancun", 7, 2)
        assert isinstance(budget, dict)
        assert "total" in budget
        assert "flights" in budget
        assert "rail_alternative" in budget

    def test_validate_suggestions(self):
        """Test suggestion validation."""
        dest = DestinationRecommendation(
            destination="Cancun",
            country="Mexico",
            description="Beach paradise",
            estimated_cost=2000,
            duration_days=7,
            highlights=[],
            best_time_to_visit="Winter",
            tripadvisor_url="https://www.tripadvisor.com"
        )
        validation = self.agent.validate_suggestions([dest])
        assert validation["validated"] == True
        assert len(validation["sources_verified"]) > 0

    def test_chat(self):
        """Test chat functionality."""
        response = self.agent.chat("Hello!")
        assert isinstance(response, str)
        assert len(self.agent.conversation_history) == 3  # System + user + assistant


class TestModels:
    """Test cases for data models."""

    def test_traveler_model(self):
        """Test Traveler model."""
        traveler = Traveler(
            name="John",
            age=30,
            preferences=["beach", "food"]
        )
        assert traveler.name == "John"
        assert traveler.age == 30

    def test_trip_details_model(self):
        """Test TripDetails model."""
        trip = TripDetails(
            destination="Bali",
            duration_days=7,
            budget=2000,
            travel_style=TravelStyle.BEACH
        )
        assert trip.destination == "Bali"
        assert trip.duration_days == 7


class TestUtilities:
    """Test cases for utility functions."""

    def test_format_currency(self):
        """Test currency formatting."""
        assert format_currency(1000) == "$1,000.00"
        assert format_currency(1234.56) == "$1,234.56"

    def test_split_budget(self):
        """Test budget splitting."""
        total = 2000
        breakdown = split_budget(total)
        assert sum(breakdown.values()) == pytest.approx(total)

    def test_split_budget_custom(self):
        """Test custom budget split."""
        custom_percentages = {
            "flights": 0.50,
            "accommodation": 0.30,
            "food": 0.20
        }
        breakdown = split_budget(1000, custom_percentages)
        assert breakdown["flights"] == 500
        assert breakdown["accommodation"] == 300
