import logging
import os
from app.services.llm import groq_llm_service
from app.core.config import get_settings
from app.services.chat_history import chat_history_service
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)
settings = get_settings()

# Set environment variable to disable Docker requirement
os.environ["AUTOGEN_USE_DOCKER"] = "False"

class ChatAgentService:
    """Service for managing chat agents using Groq"""
    
    def __init__(self):
        """Initialize the chat agent service"""
        self.system_message = "You are a helpful AI assistant powered by Groq LLM. Provide accurate, concise, and helpful responses. You specialize in GRC (Governance, Risk, and Compliance) topics and policies."
        logger.debug("Initializing chat agent service")
        logger.debug("Chat agent service initialized")
        
        # Maximum number of previous messages to include for context
        self.max_history_length = 20  # Increased from 10
    
    async def generate_response(self, message: str, session_id: Optional[str] = None) -> str:
        """
        Generate a response using Groq LLM with conversation memory
        
        Args:
            message: The user's message
            session_id: Optional session ID for persistent conversations
        
        Returns:
            The agent's response
        """
        try:
            logger.debug(f"Generating response to: {message}")
            logger.debug(f"Using session ID: {session_id}")
            
            # Save the user message to history
            chat_history_service.add_message(message, "user", session_id)
            
            # Build message history for context
            messages = []
            
            # Add system message
            messages.append({"role": "system", "content": self.system_message})
            
            # Add conversation history
            history = chat_history_service.get_message_history(session_id, self.max_history_length)
            logger.debug(f"Retrieved {len(history)} message(s) from history for context")
            
            # Include full conversation history
            if history:
                # Add all messages from history
                messages.extend(history)
                logger.debug(f"Added all messages from history to context")
            
            # Log the full conversation context being sent to the LLM
            logger.debug(f"Full conversation context (first 100 chars of each message):")
            for idx, msg in enumerate(messages):
                logger.debug(f"[{idx}] {msg['role']}: {msg['content'][:100]}...")
            
            # Generate response
            response = await groq_llm_service.generate_response(messages)
            logger.debug(f"Generated response: {response[:100]}...")
            
            # Save assistant response to history
            added_message = chat_history_service.add_message(response, "assistant", session_id)
            if added_message:
                logger.debug(f"Successfully saved assistant response to history with session_id: {session_id}")
            else:
                logger.warning(f"Failed to save assistant response to history with session_id: {session_id}")
            
            return response
                
        except Exception as e:
            logger.error(f"Error generating agent response: {str(e)}", exc_info=True)
            error_response = f"I'm sorry, I encountered an error while processing your request. Error: {str(e)}"
            
            # Save error response to history
            chat_history_service.add_message(error_response, "assistant", session_id)
            
            return error_response

# Create a singleton instance
chat_agent_service = ChatAgentService()
