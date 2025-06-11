import os
from typing import Optional, List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings"""
    
    # API settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Navigation Chatbot"
    
    # CORS settings
    CORS_ORIGINS: list[str] = ["*"]
    
    # Neo4j settings
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USERNAME: str = os.getenv("NEO4J_USERNAME", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "password")
    NEO4J_DATABASE: Optional[str] = os.getenv("NEO4J_DATABASE", None)
    
    # GROQ API settings
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    # LangChain settings
    LANGCHAIN_VERBOSE: bool = os.getenv("LANGCHAIN_VERBOSE", "False").lower() == "true"
    LANGCHAIN_TRACING: bool = os.getenv("LANGCHAIN_TRACING", "False").lower() == "true"
    
    # Vector embedding settings
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

def validate_settings(settings: Settings) -> None:
    """Validate that required settings are set"""
    errors = []
    
    # Validate GROQ API Key
    if not settings.GROQ_API_KEY:
        errors.append("GROQ_API_KEY environment variable is not set or is empty")
    
    # Validate Neo4j connection settings
    if not settings.NEO4J_URI:
        errors.append("NEO4J_URI environment variable is not set or is empty")
    if not settings.NEO4J_USERNAME:
        errors.append("NEO4J_USERNAME environment variable is not set or is empty")
    if not settings.NEO4J_PASSWORD:
        errors.append("NEO4J_PASSWORD environment variable is not set or is empty")
    
    # Validate other required settings
    if not settings.EMBEDDING_MODEL:
        errors.append("EMBEDDING_MODEL environment variable is not set or is empty")
    
    # Raise error with all validation failures if any
    if errors:
        raise ValueError(f"Configuration validation failed: {', '.join(errors)}")
    
    # Log warning for default password
    if settings.NEO4J_PASSWORD == "password":
        import logging
        logger = logging.getLogger(__name__)
        logger.warning("Using default Neo4j password. This is not secure for production environments.")

# Create settings instance
settings = Settings()

# Validate settings
try:
    validate_settings(settings)
except ValueError as e:
    import logging
    logging.getLogger(__name__).error(f"Configuration error: {str(e)}")
    # Don't raise here - allow the application to start but log the error
    # This way the API can still return helpful error messages 