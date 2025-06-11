import logging
import os
from typing import Optional, Dict, Any, List

from langchain_groq import ChatGroq
from langchain_core.callbacks.manager import CallbackManager
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.messages import HumanMessage
from app.core.config import settings

# Configure logger
logger = logging.getLogger(__name__)

# Global LLM instance
_llm: Optional[ChatGroq] = None

def get_llm(streaming: bool = False) -> ChatGroq:
    """Get or create a GROQ LLM instance"""
    global _llm
    
    # Create a new instance for streaming
    if streaming:
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        return ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name=settings.GROQ_MODEL,
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()],
            verbose=settings.LANGCHAIN_VERBOSE,
            temperature=0.0
        )
    
    # Use cached instance for non-streaming
    if _llm is None:
        try:
            logger.info(f"Initializing GROQ LLM with model: {settings.GROQ_MODEL}")
            _llm = ChatGroq(
                api_key=settings.GROQ_API_KEY,
                model_name=settings.GROQ_MODEL,
                streaming=False,
                verbose=settings.LANGCHAIN_VERBOSE,
                temperature=0.0
            )
            logger.info("GROQ LLM initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize GROQ LLM: {str(e)}")
            raise
    
    return _llm

def get_llm_response(query: str, context: Optional[str] = None) -> str:
    """Get a response from the LLM for a given query"""
    try:
        llm = get_llm()
        
        # Prepare prompt with context if provided
        if context:
            prompt = f"""
            I need information related to the following query: {query}
            
            Here is relevant context information:
            {context}
            
            Please provide a helpful response based on this context.
            """
        else:
            prompt = query
        
        # Get response
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    
    except Exception as e:
        logger.error(f"Error getting LLM response: {str(e)}")
        return f"Sorry, I encountered an error processing your request: {str(e)}"

def get_llm_streaming_response(query: str, context: Optional[str] = None):
    """Get a streaming response from the LLM for a given query"""
    try:
        llm = get_llm(streaming=True)
        
        # Prepare prompt with context if provided
        if context:
            prompt = f"""
            I need information related to the following query: {query}
            
            Here is relevant context information:
            {context}
            
            Please provide a helpful response based on this context.
            """
        else:
            prompt = query
        
        # Get streaming response
        for chunk in llm.stream([HumanMessage(content=prompt)]):
            yield chunk.content
    
    except Exception as e:
        logger.error(f"Error getting streaming LLM response: {str(e)}")
        yield f"Sorry, I encountered an error processing your request: {str(e)}" 