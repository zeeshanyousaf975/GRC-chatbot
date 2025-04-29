from fastapi import APIRouter, HTTPException, Cookie, Header
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
import uuid
from app.services.agent import chat_agent_service
from app.services.chat_history import chat_history_service

# Setup logging
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter()

# Define request/response models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    system_prompt: Optional[str] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    error: Optional[str] = None
    success: bool = True
    session_id: Optional[str] = None

@router.post("/send", response_model=ChatResponse)
async def send_message(
    chat_request: ChatRequest,
    session_id: Optional[str] = Cookie(None),
    x_session_id: Optional[str] = Header(None)
):
    """
    Endpoint to send a message to the chat agent and get a response
    Supports session tracking via cookies, headers, or request body
    """
    try:
        logger.debug(f"Received chat request: {chat_request}")
        
        # Determine session ID (prioritize request body, then header, then cookie)
        active_session_id = chat_request.session_id or x_session_id or session_id
        
        # Extract the last user message
        last_message = None
        for message in reversed(chat_request.messages):
            if message.role == "user":
                last_message = message.content
                break
        
        if not last_message:
            raise HTTPException(status_code=400, detail="No user message found in the request")
        
        # Generate response using Groq with memory
        response = await chat_agent_service.generate_response(last_message, active_session_id)
        
        # Get or create a session ID
        if not active_session_id:
            active_session_id = chat_history_service.default_session_id
        
        return ChatResponse(
            response=response,
            success=True,
            error=None,
            session_id=active_session_id
        )
    except Exception as e:
        logger.error(f"Error processing chat request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", response_model=None)
async def chat(
    request: Dict[str, Any],
    session_id: Optional[str] = Cookie(None),
    x_session_id: Optional[str] = Header(None)
):
    """
    Simple chat endpoint that matches the frontend's expectations
    Accepts a simple {message: string} format
    Supports session tracking via cookies, headers, or request body
    """
    try:
        logger.debug(f"Received simple chat request: {request}")
        
        # Get message and session ID
        message = request.get("message", "")
        request_session_id = request.get("session_id")
        
        # Determine session ID (prioritize request body, then header, then cookie)
        active_session_id = request_session_id or x_session_id or session_id
        
        logger.debug(f"Session ID sources - Request: {request_session_id}, Header: {x_session_id}, Cookie: {session_id}")
        logger.debug(f"Using active session ID: {active_session_id}")
        
        if not message:
            return {
                "response": "Please provide a message to get a response.",
                "success": False,
                "error": "No message provided",
                "session_id": active_session_id or chat_history_service.default_session_id
            }
        
        # If no session ID is provided, create a new one or use the default
        if not active_session_id:
            active_session_id = chat_history_service.default_session_id
            logger.debug(f"No session ID provided, using default: {active_session_id}")
        
        # Ensure the conversation exists
        active_session_id = chat_history_service.get_or_create_conversation(active_session_id)
        logger.debug(f"Ensured conversation exists with ID: {active_session_id}")
        
        # Generate response using Groq with memory
        response = await chat_agent_service.generate_response(message, active_session_id)
        
        # Make sure to return a properly structured response
        logger.debug(f"Returning response with session ID: {active_session_id}")
        return {
            "response": response,
            "success": True,
            "error": None,
            "session_id": active_session_id
        }
    except Exception as e:
        logger.error(f"Error processing simple chat request: {e}", exc_info=True)
        error_message = str(e)
        
        # Return the session ID even in case of error
        active_session_id = request.get("session_id") or x_session_id or session_id or chat_history_service.default_session_id
        
        # Ensure the conversation exists even for error responses
        active_session_id = chat_history_service.get_or_create_conversation(active_session_id)
        
        return {
            "response": f"Sorry, I encountered an error: {error_message}",
            "success": False,
            "error": error_message,
            "session_id": active_session_id
        }

@router.get("/history")
async def get_chat_history(
    session_id: Optional[str] = None, 
    limit: int = 10,
    x_session_id: Optional[str] = Header(None),
    cookie_session_id: Optional[str] = Cookie(None, alias="session_id")
):
    """Get the chat history for a session"""
    # Determine which session ID to use
    active_session_id = session_id or x_session_id or cookie_session_id
    
    # If no session ID is provided, use the default
    if not active_session_id:
        active_session_id = chat_history_service.default_session_id
    
    # Get messages
    messages = chat_history_service.get_messages(active_session_id, limit)
    
    # Convert to serializable format
    message_list = [
        {
            "id": str(msg.id),
            "content": msg.content,
            "role": msg.role,
            "timestamp": msg.timestamp.isoformat()
        }
        for msg in messages
    ]
    
    return {
        "session_id": active_session_id,
        "messages": message_list
    }

@router.post("/clear")
async def clear_chat_history(
    session_id: Optional[str] = None,
    x_session_id: Optional[str] = Header(None),
    cookie_session_id: Optional[str] = Cookie(None, alias="session_id")
):
    """Clear the chat history for a session"""
    # Determine which session ID to use
    active_session_id = session_id or x_session_id or cookie_session_id
    
    # If no session ID is provided, use the default
    if not active_session_id:
        active_session_id = chat_history_service.default_session_id
    
    # Clear history
    success = chat_history_service.clear_conversation(active_session_id)
    
    return {
        "success": success,
        "session_id": active_session_id,
        "message": "Chat history cleared" if success else "Failed to clear chat history"
    }

@router.get("/health")
async def router_health_check():
    """Health check endpoint for the chat router"""
    return {"status": "healthy"}

@router.get("/test")
async def test_endpoint():
    """Test endpoint for the chat router"""
    return {"message": "Chat router is working!"}

@router.get("/debug")
async def debug_chat_status(
    session_id: Optional[str] = None,
    x_session_id: Optional[str] = Header(None),
    cookie_session_id: Optional[str] = Cookie(None, alias="session_id")
):
    """
    Debug endpoint to check conversation status and memory
    Only for development use
    """
    try:
        # Determine which session ID to use
        active_session_id = session_id or x_session_id or cookie_session_id or chat_history_service.default_session_id
        
        # Get active conversations
        all_conversations = chat_history_service.list_all_conversations()
        
        # Get current conversation if it exists
        current_conversation = None
        current_messages = []
        
        if active_session_id in all_conversations:
            conversation = chat_history_service.get_conversation(active_session_id)
            if conversation:
                current_conversation = {
                    "id": str(conversation.id),
                    "created_at": conversation.created_at.isoformat(),
                    "updated_at": conversation.updated_at.isoformat(),
                    "message_count": len(conversation.messages)
                }
                
                # Get message summaries
                for msg in conversation.messages:
                    current_messages.append({
                        "id": str(msg.id),
                        "role": msg.role,
                        "timestamp": msg.timestamp.isoformat(),
                        "content_preview": msg.content[:100] + ("..." if len(msg.content) > 100 else "")
                    })
        
        return {
            "status": "ok",
            "active_session_id": active_session_id,
            "default_session_id": chat_history_service.default_session_id,
            "is_using_default": active_session_id == chat_history_service.default_session_id,
            "active_conversations_count": len(all_conversations),
            "active_conversations": all_conversations,
            "current_conversation": current_conversation,
            "message_history": current_messages,
            "max_history_length": chat_agent_service.max_history_length
        }
    except Exception as e:
        logger.error(f"Error in debug endpoint: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error": str(e)
        }