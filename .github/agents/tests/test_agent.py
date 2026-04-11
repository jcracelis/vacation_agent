"""Tests for the Vacation Agent."""

import pytest
from src.agent import VacationAgent, LLM_PROVIDERS, _detect_provider
from src.agent import DestinationRecommendation, Transportation, Activity
from src.models import Traveler, TripDetails, TravelStyle
from src.utils import format_currency, split_budget


# ─── VacationAgent Core Tests ───────────────────────────────────────────────


class TestVacationAgent:
    """Test cases for VacationAgent class."""

    def setup_method(self):
        """Set up fresh agent for each test."""
        self.agent = VacationAgent()

    # ─── Initialization ─────────────────────────────────────────────────

    def test_init_default(self):
        """Test default agent initialization — Ollama should be the default."""
        assert self.agent.provider == "ollama"
        assert self.agent.model_name == "llama3"
        assert len(self.agent.conversation_history) == 1  # system prompt only
        assert self.agent.conversation_history[0]["role"] == "system"
        assert self.agent.user_preferences == {}
        assert "tripadvisor.com" in self.agent.APPROVED_REVIEW_SOURCES
        assert "aa.com" in self.agent.APPROVED_AIRLINES

    def test_init_qwen_provider(self):
        """Test Qwen provider initialization."""
        agent = VacationAgent(provider="qwen", model_name="qwen-plus")
        assert agent.provider == "qwen"
        assert agent.model_name == "qwen-plus"

    def test_init_ollama_provider(self):
        """Test Ollama provider initialization."""
        agent = VacationAgent(provider="ollama", model_name="llama3")
        assert agent.provider == "ollama"
        assert agent.model_name == "llama3"

    def test_init_ollama_custom_url(self):
        """Test Ollama with custom base URL."""
        agent = VacationAgent(
            provider="ollama",
            model_name="mistral",
            ollama_base_url="http://192.168.1.50:11434"
        )
        assert agent.ollama_base_url == "http://192.168.1.50:11434"
        assert agent.get_base_url() == "http://192.168.1.50:11434/v1/chat/completions"

    # ─── Provider Configuration ─────────────────────────────────────────

    def test_llm_providers_config(self):
        """Test that all LLM providers are properly configured."""
        for name in ("openai", "qwen", "ollama"):
            assert name in LLM_PROVIDERS
            cfg = LLM_PROVIDERS[name]
            assert "base_url" in cfg
            assert "models" in cfg
            assert len(cfg["models"]) > 0
            assert "display_name" in cfg

    def test_get_api_key_openai(self):
        """Test getting OpenAI API key."""
        agent = VacationAgent(provider="openai", openai_api_key="sk-test-key")
        assert agent.get_api_key() == "sk-test-key"

    def test_get_api_key_qwen(self):
        """Test getting Qwen API key."""
        agent = VacationAgent(provider="qwen", qwen_api_key="qwen-test-key")
        assert agent.get_api_key() == "qwen-test-key"

    def test_get_api_key_ollama_is_none(self):
        """Test that Ollama returns None for API key (not needed)."""
        agent = VacationAgent(provider="ollama")
        assert agent.get_api_key() is None

    def test_get_base_url_openai(self):
        """Test OpenAI base URL."""
        agent = VacationAgent(provider="openai")
        assert "api.openai.com" in agent.get_base_url()

    def test_get_base_url_qwen(self):
        """Test Qwen base URL."""
        agent = VacationAgent(provider="qwen")
        assert "dashscope.aliyuncs.com" in agent.get_base_url()

    def test_get_base_url_ollama(self):
        """Test Ollama base URL."""
        agent = VacationAgent(provider="ollama", ollama_base_url="http://localhost:11434")
        assert agent.get_base_url() == "http://localhost:11434/v1/chat/completions"

    def test_get_provider_config(self):
        """Test getting provider configuration."""
        agent = VacationAgent()
        config = agent.get_provider_config()
        assert "base_url" in config
        assert "models" in config
        assert "requires_api_key" in config
        assert "display_name" in config

    # ─── LLM Availability ───────────────────────────────────────────────

    def test_is_llm_available_no_key(self):
        """Test LLM unavailable when no API key is set."""
        agent = VacationAgent(provider="openai")
        assert agent.is_llm_available() is False

    def test_is_llm_available_with_key(self):
        """Test LLM available when API key is set."""
        agent = VacationAgent(provider="openai", openai_api_key="sk-test")
        assert agent.is_llm_available() is True

    def test_is_llm_available_ollama(self):
        """Test Ollama availability check (will be False if server not running)."""
        agent = VacationAgent(provider="ollama")
        # This tests connectivity, not just config
        result = agent.is_llm_available()
        # Could be True (server running) or False (server not running) — both valid
        assert isinstance(result, bool)

    def test_check_ollama_alive_not_running(self):
        """Test Ollama connectivity check returns False when server is down."""
        agent = VacationAgent(provider="ollama", ollama_base_url="http://localhost:99999")
        assert agent._check_ollama_alive() is False

    # ─── Provider Auto-Detection ─────────────────────────────────────────

    def test_detect_provider_explicit(self):
        """Test explicit provider selection."""
        assert _detect_provider("qwen") == "qwen"
        assert _detect_provider("ollama") == "ollama"
        assert _detect_provider("openai") == "openai"

    def test_detect_provider_no_hint_defaults_to_ollama(self):
        """Test auto-detection defaults to Ollama when no hint is given."""
        result = _detect_provider()
        assert result == "ollama"

    def test_detect_provider_invalid_hint(self):
        """Test invalid hint falls back to Ollama (the default)."""
        result = _detect_provider("invalid_provider")
        assert result == "ollama"

    # ─── User Interaction ───────────────────────────────────────────────

    def test_greet(self):
        """Test greeting functionality."""
        greeting = self.agent.greet()
        assert isinstance(greeting, str)
        assert len(greeting) > 0
        assert len(self.agent.conversation_history) == 2  # system + greeting

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

    # ─── Source Validation ──────────────────────────────────────────────

    def test_validate_source_approved(self):
        """Test source validation for approved sources."""
        assert self.agent.validate_source("https://www.tripadvisor.com/Attraction_Review")
        assert self.agent.validate_source("https://www.aa.com/flights")
        assert self.agent.validate_source("https://www.southwest.com")
        assert self.agent.validate_source("https://www.delta.com")
        assert self.agent.validate_source("https://www.amtrak.com")

    def test_validate_source_unapproved(self):
        """Test source validation rejects unapproved sources."""
        assert not self.agent.validate_source("https://www.expedia.com")
        assert not self.agent.validate_source("https://www.booking.com")
        assert not self.agent.validate_source("https://www.yelp.com")

    # ─── Planning Methods ───────────────────────────────────────────────

    def test_plan_destination(self):
        """Test destination planning returns structured data."""
        result = self.agent.plan_destination("beach", 7, 3000)
        assert isinstance(result, DestinationRecommendation)
        assert result.tripadvisor_url is not None
        assert self.agent.validate_source(result.tripadvisor_url)

    def test_find_transportation(self):
        """Test transportation finding."""
        transport = self.agent.find_transportation("Chicago", "Miami", "2026-05-15")
        assert len(transport) > 0
        assert isinstance(transport[0], Transportation)
        assert transport[0].is_nonstop is True
        assert self.agent.validate_source(transport[0].booking_url)

    def test_suggest_activities(self):
        """Test activity suggestions."""
        activities = self.agent.suggest_activities("Cancun", "beach", 7)
        assert len(activities) > 0
        assert isinstance(activities[0], Activity)
        assert activities[0].suitable_for_adults_only is True

    def test_generate_itinerary(self):
        """Test itinerary generation."""
        itinerary = self.agent.generate_itinerary("Cancun", 7)
        assert len(itinerary) == 7
        for i, day in enumerate(itinerary):
            assert day.day_number == i + 1

    def test_estimate_budget(self):
        """Test budget estimation structure."""
        budget = self.agent.estimate_budget("Cancun", 7, 2)
        assert isinstance(budget, dict)
        for key in ("flights", "accommodation", "food", "activities", "rail_alternative", "total"):
            assert key in budget

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
        assert validation["validated"] is True
        assert len(validation["sources_verified"]) > 0

    def test_chat(self):
        """Test chat functionality."""
        response = self.agent.chat("Hello!")
        assert isinstance(response, str)
        assert len(response) > 0
        assert len(self.agent.conversation_history) == 3  # system + user + assistant


# ─── Model Tests ──────────────────────────────────────────────────────────────


class TestModels:
    """Test cases for data models."""

    def test_traveler_model(self):
        """Test Traveler model creation."""
        traveler = Traveler(name="John", age=30, preferences=["beach", "food"])
        assert traveler.name == "John"
        assert traveler.age == 30

    def test_trip_details_model(self):
        """Test TripDetails model creation."""
        trip = TripDetails(
            destination="Bali",
            duration_days=7,
            budget=2000,
            travel_style=TravelStyle.BEACH
        )
        assert trip.destination == "Bali"
        assert trip.duration_days == 7


# ─── Utility Tests ────────────────────────────────────────────────────────────


class TestUtilities:
    """Test cases for utility functions."""

    def test_format_currency(self):
        """Test currency formatting."""
        assert format_currency(1000) == "$1,000.00"
        assert format_currency(1234.56) == "$1,234.56"

    def test_split_budget(self):
        """Test default budget split."""
        total = 2000
        breakdown = split_budget(total)
        assert sum(breakdown.values()) == pytest.approx(total)

    def test_split_budget_custom(self):
        """Test custom budget split percentages."""
        custom = {"flights": 0.50, "accommodation": 0.30, "food": 0.20}
        breakdown = split_budget(1000, custom)
        assert breakdown["flights"] == 500
        assert breakdown["accommodation"] == 300
        assert breakdown["food"] == 200
