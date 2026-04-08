"""Data models for the Vacation Agent."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class TravelStyle(str, Enum):
    """Enumeration of travel styles."""
    BEACH = "beach"
    MOUNTAIN = "mountain"
    CITY = "city"
    ADVENTURE = "adventure"
    CULTURAL = "cultural"
    RELAXATION = "relaxation"
    ROMANTIC = "romantic"
    FAMILY = "family"


class Season(str, Enum):
    """Enumeration of seasons."""
    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall"
    WINTER = "winter"


class Traveler(BaseModel):
    """Model for a traveler."""
    name: str
    age: Optional[int] = None
    preferences: list[str] = Field(default_factory=list)
    restrictions: list[str] = Field(default_factory=list)


class TripDetails(BaseModel):
    """Model for trip details."""
    destination: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    duration_days: int
    budget: float
    travelers: list[Traveler] = Field(default_factory=list)
    travel_style: Optional[TravelStyle] = None
    preferred_season: Optional[Season] = None
    special_requests: list[str] = Field(default_factory=list)


class Activity(BaseModel):
    """Model for an activity."""
    name: str
    description: str
    duration_hours: float
    cost: float
    location: str
    category: str


class Accommodation(BaseModel):
    """Model for accommodation."""
    name: str
    type: str  # hotel, hostel, Airbnb, resort, etc.
    cost_per_night: float
    rating: Optional[float] = None
    amenities: list[str] = Field(default_factory=list)
    location: str
