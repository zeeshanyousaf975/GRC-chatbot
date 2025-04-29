from groq import Groq
import logging
import time
import json
from app.core.config import get_settings
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)
settings = get_settings()

class GroqLLMService:
    """Service for interacting with Groq LLM API"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize the Groq LLM service"""
        self.api_key = api_key or settings.GROQ_API_KEY
        self.model = model or settings.GROQ_MODEL
        
        if not self.api_key:
            logger.error("GROQ_API_KEY is not set")
            raise ValueError("GROQ_API_KEY is required to use Groq LLM service")
        
        self.client = Groq(api_key=self.api_key)
        logger.debug(f"Initialized Groq LLM service with model: {self.model}")
    
    async def generate_response(self, messages: List[Dict[str, str]], 
                              max_tokens: int = settings.AUTOGEN_MAX_TOKENS,
                              temperature: float = settings.AUTOGEN_TEMPERATURE,
                              max_retries: int = 3) -> str:
        """Generate a response from the LLM with retries"""
        retries = 0
        last_error = None
        
        while retries < max_retries:
            try:
                logger.debug(f"Generating response with model {self.model}, max_tokens={max_tokens}, temperature={temperature}")
                logger.debug(f"Messages: {messages}")
                
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                
                response = completion.choices[0].message.content
                logger.debug(f"Generated response: {response}")
                return response
                
            except Exception as e:
                retries += 1
                last_error = e
                logger.warning(f"Error generating response from Groq (attempt {retries}/{max_retries}): {str(e)}")
                
                if retries < max_retries:
                    # Exponential backoff
                    wait_time = 2 ** retries
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed after {max_retries} attempts: {str(e)}", exc_info=True)
                    raise
        
        # If we reach here, all retries failed
        logger.error(f"All retries failed: {str(last_error)}")
        raise last_error

# Singleton instance
groq_llm_service = GroqLLMService() 