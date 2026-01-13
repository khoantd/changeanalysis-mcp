"""Configuration for API clients."""

import os
import logging
from dataclasses import dataclass
from typing import Optional, Literal


@dataclass
class APIConfig:
    """Configuration for API endpoints."""
    base_url: str
    timeout: float = 30.0
    api_key: Optional[str] = None
    auth_method: Literal["bearer", "x-api-key"] = "x-api-key"
    """Authentication method: 'bearer' uses Authorization header, 'x-api-key' uses X-API-Key header."""


def get_config_from_env() -> APIConfig:
    """
    Create APIConfig from environment variables.
    
    Environment variables:
        CHANGE_ANALYSIS_API_BASE_URL: Base URL for the API (required)
        CHANGE_ANALYSIS_API_KEY: API key for authentication (optional)
        CHANGE_ANALYSIS_API_TIMEOUT: Request timeout in seconds (default: 30.0)
        CHANGE_ANALYSIS_AUTH_METHOD: Authentication method - 'bearer' or 'x-api-key' (default: 'x-api-key')
    
    Returns:
        APIConfig instance configured from environment variables
        
    Raises:
        ValueError: If required environment variables are missing
    """
    base_url = os.getenv("CHANGE_ANALYSIS_API_BASE_URL")
    if not base_url:
        raise ValueError(
            "CHANGE_ANALYSIS_API_BASE_URL environment variable is required. "
            "Please set it to your API base URL."
        )
    
    api_key = os.getenv("CHANGE_ANALYSIS_API_KEY")
    timeout_str = os.getenv("CHANGE_ANALYSIS_API_TIMEOUT", "30.0")
    auth_method_raw = os.getenv("CHANGE_ANALYSIS_AUTH_METHOD", "x-api-key")
    
    # Normalize auth_method to lowercase for consistency
    auth_method = auth_method_raw.lower() if auth_method_raw else "x-api-key"
    
    try:
        timeout = float(timeout_str)
    except ValueError:
        raise ValueError(f"Invalid CHANGE_ANALYSIS_API_TIMEOUT value: {timeout_str}")
    
    if auth_method not in ("bearer", "x-api-key"):
        raise ValueError(
            f"Invalid CHANGE_ANALYSIS_AUTH_METHOD: {auth_method_raw}. "
            "Must be 'bearer' or 'x-api-key'"
        )
    
    return APIConfig(
        base_url=base_url,
        timeout=timeout,
        api_key=api_key,
        auth_method=auth_method
    )


# Default API configuration - tries environment variables first, falls back to defaults
# Note: In production, always use environment variables via get_config_from_env()
try:
    DEFAULT_CONFIG = get_config_from_env()
except ValueError as e:
    # Fallback for development - should not be used in production
    logger = logging.getLogger("changeanalysis_mcp.config")
    logger.warning(
        f"Failed to load config from environment: {e}. "
        "Using fallback configuration. This should not be used in production."
    )
    
    base_url = os.getenv("CHANGE_ANALYSIS_API_BASE_URL", "http://72.60.233.159:8092")
    api_key = os.getenv("CHANGE_ANALYSIS_API_KEY")
    auth_method_raw = os.getenv("CHANGE_ANALYSIS_AUTH_METHOD", "x-api-key")
    auth_method = auth_method_raw.lower() if auth_method_raw else "x-api-key"
    
    if not api_key:
        logger.warning(
            "CHANGE_ANALYSIS_API_KEY not set. API requests will be made without authentication. "
            "Set CHANGE_ANALYSIS_API_KEY environment variable for production use."
        )
    
    DEFAULT_CONFIG = APIConfig(
        base_url=base_url,
        timeout=float(os.getenv("CHANGE_ANALYSIS_API_TIMEOUT", "30.0")),
        api_key=api_key,
        auth_method=auth_method
    )
