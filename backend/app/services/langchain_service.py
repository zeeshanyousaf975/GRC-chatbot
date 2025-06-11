import logging
from typing import Dict, Any, List, Optional
import os

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq

from app.core.config import settings

logger = logging.getLogger(__name__)

class LangChainService:
    """Service for LangChain integration"""
    
    def __init__(self):
        """Initialize the LangChain service with GROQ LLM"""
        try:
            self.llm = ChatGroq(
                api_key=settings.GROQ_API_KEY,
                model_name=settings.GROQ_MODEL,
                temperature=0.3,
                max_tokens=1024,
            )
            logger.info(f"Initialized GROQ LLM with model: {settings.GROQ_MODEL}")
        except Exception as e:
            logger.error(f"Failed to initialize GROQ LLM: {str(e)}")
            # Initialize with a fallback or None, but let the service start
            self.llm = None
            
    def create_navigation_chain(self, context: List[Dict[str, Any]]) -> Any:
        """
        Create a chain for navigation queries
        
        Args:
            context: List of context documents from vector search
            
        Returns:
            A runnable chain for processing navigation queries
        """
        if not self.llm:
            logger.error("LLM not initialized. Check your API key and connectivity.")
            raise ValueError("LLM service is not available")
            
        # Convert context to a formatted string
        def format_context(context_docs):
            if not context_docs:
                return "No relevant information found."
                
            formatted_context = "\n\n".join([
                f"Source: {doc.get('source', 'Unknown')}\nContent: {doc.get('content', '')}"
                for doc in context_docs
            ])
            return formatted_context
            
        # System prompt
        system_prompt = """You are a helpful navigation assistant. 
        Your goal is to help users navigate to their destination based on their queries.
        Use the provided context information to answer navigation questions.
        If you don't know the answer or don't have enough information, say so rather than making something up.
        Always provide clear, concise directions when possible.
        
        Context information:
        {context}
        """
        
        # Create the chain
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}")
            ])
            
            chain = (
                {"context": lambda x: format_context(x["context"]), 
                 "question": lambda x: x["question"],
                 "chat_history": lambda x: x.get("chat_history", [])}
                | prompt
                | self.llm
                | StrOutputParser()
            )
            
            return chain
        except Exception as e:
            logger.error(f"Error creating navigation chain: {str(e)}")
            raise RuntimeError(f"Failed to create LangChain chain: {str(e)}")
    
    async def process_query(self, 
                     question: str, 
                     context: List[Dict[str, Any]],
                     chat_history: Optional[List] = None) -> str:
        """
        Process a user query with the navigation chain
        
        Args:
            question: User question
            context: Context information from vector search
            chat_history: Optional chat history
            
        Returns:
            Response from the LLM
        """
        if not chat_history:
            chat_history = []
            
        try:
            # Create the chain for this query
            chain = self.create_navigation_chain(context)
            
            # Convert chat history to the expected format if it exists
            formatted_history = []
            for msg in chat_history:
                if msg["type"] == "human":
                    formatted_history.append(HumanMessage(content=msg["content"]))
                elif msg["type"] == "ai":
                    formatted_history.append(SystemMessage(content=msg["content"]))
            
            # Run the chain
            response = chain.invoke({
                "question": question,
                "context": context,
                "chat_history": formatted_history
            })
            
            return response
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return "I'm sorry, I encountered an error processing your request. Please try again later."

# Create a singleton instance
langchain_service = LangChainService() 