import logging
from typing import Dict, List, Optional
import uuid
from datetime import datetime
from app.models.chat import Message, Conversation

logger = logging.getLogger(__name__)

class ChatHistoryService:
    """Service for managing chat history"""
    
    def __init__(self):
        """Initialize chat history service"""
        # Store conversations by session ID
        self.conversations: Dict[str, Conversation] = {}
        # Store current session ID for anonymous users
        self.default_session_id = str(uuid.uuid4())
        logger.debug(f"Chat history service initialized with default session {self.default_session_id}")
    
    def create_conversation(self, session_id: Optional[str] = None) -> str:
        """
        Create a new conversation and return the conversation ID
        If session_id is provided, use it; otherwise generate a new one
        """
        conversation_id = session_id or str(uuid.uuid4())
        conversation = Conversation(id=conversation_id)
        self.conversations[conversation_id] = conversation
        logger.debug(f"Created new conversation with ID: {conversation_id}")
        return conversation_id
    
    def get_or_create_conversation(self, session_id: Optional[str] = None) -> str:
        """Get existing conversation or create a new one if it doesn't exist"""
        conversation_id = session_id or self.default_session_id
        logger.debug(f"Looking for conversation with ID: {conversation_id}")
        
        if conversation_id not in self.conversations:
            logger.debug(f"Conversation not found, creating new one with ID: {conversation_id}")
            return self.create_conversation(conversation_id)
        
        logger.debug(f"Found existing conversation with ID: {conversation_id}, message count: {len(self.conversations[conversation_id].messages)}")
        return conversation_id
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get a conversation by ID"""
        conversation = self.conversations.get(conversation_id)
        if not conversation:
            logger.warning(f"Conversation not found: {conversation_id}")
        else:
            logger.debug(f"Retrieved conversation {conversation_id} with {len(conversation.messages)} messages")
        return conversation
    
    def add_message(self, content: str, role: str, conversation_id: Optional[str] = None) -> Optional[Message]:
        """
        Add a message to a conversation
        If no conversation_id is provided, use the default session
        """
        conversation_id = self.get_or_create_conversation(conversation_id)
        conversation = self.get_conversation(conversation_id)
        
        if not conversation:
            logger.error(f"Failed to add message, conversation not found: {conversation_id}")
            return None
        
        message = conversation.add_message(content, role)
        logger.debug(f"Added {role} message to conversation {conversation_id}: {content[:50]}...")
        logger.debug(f"Conversation {conversation_id} now has {len(conversation.messages)} messages")
        return message
    
    def get_messages(self, conversation_id: Optional[str] = None, limit: int = 10) -> List[Message]:
        """
        Get messages from a conversation with limit
        If no conversation_id is provided, use the default session
        """
        conversation_id = conversation_id or self.default_session_id
        logger.debug(f"Getting messages for conversation: {conversation_id}, limit: {limit}")
        
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            logger.warning(f"Cannot get messages from non-existent conversation: {conversation_id}")
            return []
        
        messages = conversation.messages[-limit:] if limit > 0 else conversation.messages
        logger.debug(f"Retrieved {len(messages)} messages from conversation {conversation_id}")
        return messages
    
    def get_message_history(self, conversation_id: Optional[str] = None, limit: int = 10) -> List[Dict[str, str]]:
        """
        Get message history in format suitable for LLM context
        Returns list of dicts with role and content keys
        If no conversation_id is provided, use the default session
        """
        messages = self.get_messages(conversation_id, limit)
        formatted_messages = [{"role": msg.role, "content": msg.content} for msg in messages]
        logger.debug(f"Formatted {len(formatted_messages)} messages for LLM context")
        
        # Log the conversation history for debugging
        if formatted_messages:
            logger.debug("Message history overview:")
            for i, msg in enumerate(formatted_messages):
                logger.debug(f"  [{i}] {msg['role']}: {msg['content'][:50]}...")
        else:
            logger.debug("No message history available")
            
        return formatted_messages
    
    def clear_conversation(self, conversation_id: Optional[str] = None) -> bool:
        """
        Clear all messages from a conversation
        If no conversation_id is provided, use the default session
        """
        conversation_id = conversation_id or self.default_session_id
        logger.debug(f"Attempting to clear conversation: {conversation_id}")
        
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            logger.warning(f"Cannot clear non-existent conversation: {conversation_id}")
            return False
        
        message_count = len(conversation.messages)
        conversation.messages = []
        logger.debug(f"Cleared {message_count} messages from conversation: {conversation_id}")
        return True
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation"""
        if conversation_id in self.conversations:
            message_count = len(self.conversations[conversation_id].messages)
            del self.conversations[conversation_id]
            logger.debug(f"Deleted conversation: {conversation_id} with {message_count} messages")
            return True
        logger.warning(f"Cannot delete non-existent conversation: {conversation_id}")
        return False

    def list_all_conversations(self) -> List[str]:
        """List all active conversation IDs for debugging"""
        conv_list = list(self.conversations.keys())
        logger.debug(f"Active conversations: {len(conv_list)}")
        return conv_list

# Create singleton instance
chat_history_service = ChatHistoryService()
