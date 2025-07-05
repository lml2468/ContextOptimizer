"""
Simple logging utilities.
"""

import logging
import sys
from pathlib import Path

from ..config import settings

# Global logger instance
_logger = None

def setup_logging():
    """Setup application logging once."""
    global _logger
    
    if _logger is not None:
        return _logger
    
    # Create root logger for the app
    _logger = logging.getLogger("app")
    
    # Set level from settings
    level = getattr(logging, settings.log_level.upper())
    _logger.setLevel(level)
    
    # Clear any existing handlers
    _logger.handlers.clear()
    
    # Simple formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    _logger.addHandler(console_handler)
    
    # File handler if configured
    if settings.log_file:
        settings.log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(settings.log_file)
        file_handler.setFormatter(formatter)
        _logger.addHandler(file_handler)
    
    return _logger

def get_logger(name: str = None) -> logging.Logger:
    """Get logger instance."""
    if _logger is None:
        setup_logging()
    return _logger

# Backward compatibility
setup_logger = setup_logging
