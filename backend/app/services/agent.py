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
        
        # Store active conversations and their contexts
        self._active_contexts: Dict[str, List[Dict[str, str]]] = {}
    
    def _get_context(self, session_id: str) -> List[Dict[str, str]]:
        """Get the current context for a session"""
        if session_id not in self._active_contexts:
            self._active_contexts[session_id] = [{"role": "system", "content": self.system_message}]
        return self._active_contexts[session_id]
    
    def clear_context(self, session_id: str) -> None:
        """Clear the context for a specific session"""
        if session_id in self._active_contexts:
            del self._active_contexts[session_id]
        logger.debug(f"Cleared context for session: {session_id}")
    
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
            
            if not session_id:
                session_id = chat_history_service.default_session_id
            
            # Get current context
            context = self._get_context(session_id)
            
            # Add user message to context
            context.append({"role": "user", "content": message})
            
            # Generate response
            response = await groq_llm_service.generate_response(context)
            
            # Add response to context
            context.append({"role": "assistant", "content": response})
            
            # Update context
            self._active_contexts[session_id] = context
            
            # Save messages to chat history service
            chat_history_service.add_message(message, "user", session_id)
            chat_history_service.add_message(response, "assistant", session_id)
            
            return response
                
        except Exception as e:
            logger.error(f"Error generating agent response: {str(e)}", exc_info=True)
            error_response = f"I'm sorry, I encountered an error while processing your request. Error: {str(e)}"
            chat_history_service.add_message(error_response, "assistant", session_id)
            return error_response

# Create a singleton instance
chat_agent_service = ChatAgentService()
