import logging
import sys
from loguru import logger as loguru_logger
from app.core.config import get_settings

# Get settings
settings = get_settings()

# Configure Loguru logger
loguru_logger.remove()
loguru_logger.add(
    sys.stdout,
    level=settings.LOG_LEVEL,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)

# Create a class to convert Loguru logs to standard logging
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        loguru_logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

# Setup loggers
def setup_logging():
    # Intercept all standard logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    
    # Intercept third-party logs
    for name in logging.root.manager.loggerDict:
        if name.startswith("uvicorn") or name.startswith("fastapi"):
            logging.getLogger(name).handlers = [InterceptHandler()]
            
    loguru_logger.debug("Logging setup complete")

# Expose Loguru logger as module-level logger
logger = loguru_logger 