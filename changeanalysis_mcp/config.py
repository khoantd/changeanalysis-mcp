"""Configuration for API clients."""

from dataclasses import dataclass


@dataclass
class APIConfig:
    """Configuration for API endpoints."""
    base_url: str
    timeout: float = 30.0


# Default API configuration
DEFAULT_CONFIG = APIConfig(
    base_url="http://72.60.233.159:8092",
    timeout=30.0
)
