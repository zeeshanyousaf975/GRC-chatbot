import logging
from typing import Dict, Any

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.langchain.chains import process_navigation_query
from app.database.neo4j import get_neo4j_driver

# Configure logger
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Query request model
class QueryRequest(BaseModel):
    query: str

# Query response model
class QueryResponse(BaseModel):
    response: str
    sources: list[Dict[str, Any]]

@router.post("/query", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    _=Depends(get_neo4j_driver)  # Ensure Neo4j connection is available
) -> Dict[str, Any]:
    """
    Process a user query and return navigation recommendations
    """
    try:
        # Validate query
        if not request.query or len(request.query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Process query
        logger.info(f"Processing query: {request.query}")
        result = process_navigation_query(request.query)
        
        return result
    
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}") 