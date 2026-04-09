"""Utility functions for the Vacation Agent.

This module provides helper functions for configuration management,
data formatting, validation, and project structure operations.

Functions:
    load_config: Load and parse YAML configuration files
    format_currency: Format numeric values as currency strings
    validate_api_key: Verify API key presence and validity
    create_directory_structure: Generate standard project directories
    days_to_nights: Convert trip duration from days to nights
    split_budget: Allocate total budget across categories by percentage
"""

import os
import yaml
from pathlib import Path
from typing import Optional


def load_config(config_path: str = "config/settings.yaml") -> dict:
    """Load configuration from YAML file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Configuration dictionary
    """
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    
    return config


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format a number as currency.
    
    Args:
        amount: The amount to format
        currency: Currency code (default: USD)
        
    Returns:
        Formatted currency string
    """
    symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥"
    }
    symbol = symbols.get(currency, "$")
    return f"{symbol}{amount:,.2f}"


def validate_api_key(api_key: Optional[str] = None) -> bool:
    """Validate that an API key is present.
    
    Args:
        api_key: API key to validate (checks env var if None)
        
    Returns:
        True if valid, False otherwise
    """
    key = api_key or os.getenv("OPENAI_API_KEY")
    return key is not None and len(key) > 0


def create_directory_structure(base_path: str = ".") -> None:
    """Create the standard directory structure for the project.
    
    Args:
        base_path: Base path to create directories under
    """
    directories = [
        "data",
        "data/raw",
        "data/processed",
        "logs",
        "outputs",
        "notebooks"
    ]
    
    for directory in directories:
        Path(base_path, directory).mkdir(parents=True, exist_ok=True)


def days_to_nights(days: int) -> int:
    """Convert trip duration in days to number of nights.
    
    Args:
        days: Number of days
        
    Returns:
        Number of nights
    """
    return max(0, days - 1)


def split_budget(total_budget: float, percentages: Optional[dict] = None) -> dict:
    """Split budget according to percentages.
    
    Args:
        total_budget: Total budget amount
        percentages: Dictionary of category percentages (should sum to 1.0)
        
    Returns:
        Dictionary with budget allocation per category
    """
    if percentages is None:
        percentages = {
            "flights": 0.30,
            "accommodation": 0.25,
            "food": 0.20,
            "activities": 0.15,
            "miscellaneous": 0.10
        }
    
    return {
        category: total_budget * percentage
        for category, percentage in percentages.items()
    }
