import logging
from typing import Dict, Any, List, Optional

from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains import create_retrieval_chain
from langchain_core.runnables import RunnablePassthrough

from app.langchain.llm import get_llm
from app.langchain.retriever import get_vector_store, retrieve_similar_nodes

# Configure logger
logger = logging.getLogger(__name__)

def create_navigation_prompt() -> PromptTemplate:
    """Create prompt template for navigation assistance"""
    template = """
    You are a helpful navigation assistant for a software platform. 
    Your goal is to help users find the right section of the platform based on their questions.
    
    USER QUERY: {query}
    
    RELEVANT NAVIGATION INFORMATION:
    {context}
    
    Based on the user's query and the navigation information provided, please help the user navigate to the most relevant section.
    Your response should include:
    
    1. A clear recommendation of which section(s) the user should navigate to
    2. The direct URL(s) to those section(s)
    3. A brief explanation of why this section is relevant to their query
    
    Format your response in a conversational way, making it easy for the user to understand and follow your recommendation.
    """
    
    return PromptTemplate(
        template=template,
        input_variables=["query", "context"]
    )

def create_navigation_chain():
    """Create a navigation chain that retrieves relevant info and generates a response"""
    try:
        # Get LLM
        llm = get_llm()
        
        # Get vector store and create retriever
        vector_store = get_vector_store()
        retriever = vector_store.as_retriever(search_kwargs={"k": 5})
        
        # Create navigation prompt
        prompt = create_navigation_prompt()
        
        # Create LLM chain for processing the context
        llm_chain = LLMChain(llm=llm, prompt=prompt)
        
        # Create document chain for combining documents
        doc_chain = StuffDocumentsChain(
            llm_chain=llm_chain,
            document_variable_name="context"
        )
        
        # Create retrieval chain
        chain = create_retrieval_chain(retriever, doc_chain)
        
        logger.info("Navigation chain created successfully")
        return chain
    
    except Exception as e:
        logger.error(f"Error creating navigation chain: {str(e)}")
        raise

def process_navigation_query(query: str) -> Dict[str, Any]:
    """Process a navigation query and return the response with source information"""
    try:
        logger.info(f"Processing navigation query: {query}")
        
        # Get similar nodes directly
        similar_nodes = retrieve_similar_nodes(query)
        
        # Check if we found any similar nodes
        if not similar_nodes:
            logger.warning("No similar nodes found for query")
            return {
                "response": "I'm sorry, I couldn't find any relevant navigation information for your query. Please try rephrasing your question or provide more details about what you're looking for.",
                "sources": []
            }
        
        # Convert nodes to context string
        context = "\n\n".join([
            f"SECTION: {node['title']}\nURL: {node['url']}\nCONTENT: {node['content']}"
            for node in similar_nodes
        ])
        
        # Generate response with LLM
        llm = get_llm()
        prompt = create_navigation_prompt()
        
        # Prepare inputs
        inputs = {
            "query": query,
            "context": context
        }
        
        # Format prompt
        formatted_prompt = prompt.format(**inputs)
        
        # Get response from LLM
        response = llm.invoke(formatted_prompt)
        
        # Prepare result
        result = {
            "response": response.content,
            "sources": [
                {
                    "title": node["title"],
                    "url": node["url"],
                    "id": node["id"]
                }
                for node in similar_nodes
            ]
        }
        
        logger.info("Navigation query processed successfully")
        return result
    
    except Exception as e:
        logger.error(f"Error processing navigation query: {str(e)}")
        return {
            "response": f"I'm sorry, I encountered an error while processing your query: {str(e)}",
            "sources": []
        } 