from pydantic import Field
from pydantic_settings import BaseSettings
import os
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    """Application settings"""
    # API settings
    API_V1_STR: str = "/api/v1"
    
    # CORS settings
    CORS_ORIGINS: str | list[str] = ["*"]
    
    # Groq API settings
    GROQ_API_KEY: str = Field(default="")
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    
    # Autogen settings
    AUTOGEN_MAX_TOKENS: int = 1024
    AUTOGEN_TEMPERATURE: float = 0.7
    
    # Logging settings
    LOG_LEVEL: str = "DEBUG"
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "allow"
    }

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    logger.debug("Loading application settings")
    return Settings() 