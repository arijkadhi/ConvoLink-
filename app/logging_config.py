"""
Logging Configuration
Maps to: Deployment - Check logs for errors
"""
import logging
import sys
from pythonjsonlogger import jsonlogger

from app.config import get_settings

settings = get_settings()


def setup_logging():
    """Configure application logging"""
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.log_level))
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, settings.log_level))
    
    # Create formatter
    if settings.environment == "production":
        # Use JSON formatter for production
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s'
        )
    else:
        # Use standard formatter for development
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger
