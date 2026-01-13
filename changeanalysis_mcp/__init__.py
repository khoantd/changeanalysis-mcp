"""Change Analysis MCP Server"""

from .config import APIConfig, DEFAULT_CONFIG, get_config_from_env
from .client import BaseAPIClient
from .services import (
    APIServiceFactory,
    ChangeRequestsService,
    SystemsService,
    FeedbacksService,
    ProjectsService,
)
from .logging_config import setup_logging, get_logger

__version__ = "0.1.0"
__all__ = [
    "APIConfig",
    "DEFAULT_CONFIG",
    "get_config_from_env",
    "BaseAPIClient",
    "APIServiceFactory",
    "ChangeRequestsService",
    "SystemsService",
    "FeedbacksService",
    "ProjectsService",
    "setup_logging",
    "get_logger",
]