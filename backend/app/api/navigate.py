import logging
from typing import Dict, Any, List

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.langchain.retriever import retrieve_similar_nodes
from app.database.neo4j import get_neo4j_driver, execute_query

# Configure logger
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Navigation request model
class NavigationRequest(BaseModel):
    query: str
    limit: int = 5

# Navigation node model
class NavigationNode(BaseModel):
    id: str
    title: str
    url: str
    score: float = 0.0

# Navigation response model
class NavigationResponse(BaseModel):
    nodes: List[NavigationNode]

@router.post("/navigate", response_model=NavigationResponse)
async def get_navigation_recommendations(
    request: NavigationRequest,
    _=Depends(get_neo4j_driver)  # Ensure Neo4j connection is available
) -> Dict[str, Any]:
    """
    Get navigation recommendations based on a query
    """
    try:
        # Validate query
        if not request.query or len(request.query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Get similar nodes
        logger.info(f"Getting navigation recommendations for query: {request.query}")
        similar_nodes = retrieve_similar_nodes(request.query, k=request.limit)
        
        # Convert to response format
        nodes = []
        for node in similar_nodes:
            nodes.append(NavigationNode(
                id=node["id"],
                title=node["title"],
                url=node["url"],
                score=node.get("score", 0.0)
            ))
        
        return {"nodes": nodes}
    
    except Exception as e:
        logger.error(f"Error getting navigation recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting navigation recommendations: {str(e)}")

@router.get("/paths/{node_id}", response_model=List[List[NavigationNode]])
async def get_navigation_paths(
    node_id: str,
    _=Depends(get_neo4j_driver)  # Ensure Neo4j connection is available
) -> List[List[Dict[str, Any]]]:
    """
    Get all possible navigation paths from root to the specified node
    """
    try:
        # Validate node ID
        if not node_id:
            raise HTTPException(status_code=400, detail="Node ID cannot be empty")
        
        # Query to find all paths from root to the specified node
        query = """
        MATCH path = (root:NavigationNode {id: 'root'})-[:CONTAINS*]->(target:NavigationNode {id: $node_id})
        RETURN [node in nodes(path) | {
            id: node.id,
            title: node.title,
            url: node.url
        }] AS path
        """
        
        params = {"node_id": node_id}
        
        # Execute query
        results = execute_query(query, params)
        
        # Process results
        paths = []
        for result in results:
            path_nodes = []
            for node_data in result["path"]:
                path_nodes.append(NavigationNode(
                    id=node_data["id"],
                    title=node_data["title"],
                    url=node_data["url"]
                ))
            paths.append(path_nodes)
        
        # If no paths found, return 404
        if not paths:
            raise HTTPException(status_code=404, detail=f"No navigation paths found for node ID: {node_id}")
        
        return paths
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        logger.error(f"Error getting navigation paths: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting navigation paths: {str(e)}") 