"""Tests for the Vacation Agent."""

import pytest
from src.agent import VacationAgent
from src.models import Traveler, TripDetails, TravelStyle, DestinationRecommendation, Itinerary
from src.utils import load_config, format_currency, split_budget


class TestVacationAgent:
    """Test cases for VacationAgent class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.agent = VacationAgent()
    
    def test_init(self):
        """Test agent initialization."""
        assert self.agent.model_name == "gpt-4"
        assert self.agent.conversation_history == []
    
    def test_plan_destination(self):
        """Test destination planning."""
        result = self.agent.plan_destination("beach", 7, 2000)
        assert isinstance(result, DestinationRecommendation)
        assert result.destination is not None
        assert result.estimated_cost <= 2000
    
    def test_generate_itinerary(self):
        """Test itinerary generation."""
        itinerary = self.agent.generate_itinerary("Bali", 7)
        assert len(itinerary) == 7
        assert all(isinstance(day, Itinerary) for day in itinerary)
    
    def test_estimate_budget(self):
        """Test budget estimation."""
        budget = self.agent.estimate_budget("Bali", 7, 2)
        assert isinstance(budget, dict)
        assert "total" in budget
        assert "flights" in budget
    
    def test_chat(self):
        """Test chat functionality."""
        response = self.agent.chat("Hello!")
        assert isinstance(response, str)
        assert len(self.agent.conversation_history) == 2


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
