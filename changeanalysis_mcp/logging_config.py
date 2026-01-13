"""Logging configuration for the MCP server."""

import logging
import sys
from typing import Optional


def setup_logging(
    level: Optional[str] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Set up logging configuration for the application.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
               Defaults to INFO, or LOG_LEVEL environment variable.
        format_string: Custom format string. Defaults to structured format.
    
    Returns:
        Configured logger instance
    """
    log_level = level or _get_log_level_from_env()
    log_format = format_string or (
        "%(asctime)s - %(name)s - %(levelname)s - "
        "%(filename)s:%(lineno)d - %(message)s"
    )
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stderr  # MCP servers should log to stderr
    )
    
    logger = logging.getLogger("changeanalysis_mcp")
    logger.setLevel(log_level)
    
    # Reduce noise from httpx and other libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    
    return logger


def _get_log_level_from_env() -> int:
    """Get log level from environment variable."""
    import os
    level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    return level_map.get(level_str, logging.INFO)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name. Defaults to 'changeanalysis_mcp'.
    
    Returns:
        Logger instance
    """
    logger_name = name or "changeanalysis_mcp"
    return logging.getLogger(logger_name)
