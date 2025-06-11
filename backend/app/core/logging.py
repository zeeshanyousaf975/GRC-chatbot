import logging
import sys
from typing import Any, Dict, List

# Configure logging formatter
class CustomFormatter(logging.Formatter):
    """Custom log formatter with colors"""
    
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    
    format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    FORMATS = {
        logging.DEBUG: grey + format_str + reset,
        logging.INFO: grey + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: bold_red + format_str + reset,
    }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def setup_logging(log_level: str = "INFO") -> None:
    """Setup logging configuration"""
    
    # Set log level
    log_level_num = getattr(logging, log_level.upper(), logging.INFO)
    
    # Configure handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(CustomFormatter())
    
    # Configure root logger
    logging.basicConfig(
        level=log_level_num,
        handlers=[handler],
        force=True,
    )
    
    # Set log level for external libraries
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)
    
    # Log configuration
    logger = logging.getLogger(__name__)
    logger.debug(f"Logging configured with level {log_level}")

def get_logger(name: str) -> logging.Logger:
    """Get a logger with the given name"""
    return logging.getLogger(name) 