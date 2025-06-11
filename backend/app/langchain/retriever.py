import logging
from typing import List, Dict, Any, Optional

from langchain_neo4j import Neo4jVector
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from app.core.config import settings
from app.langchain.embeddings import get_embeddings

# Configure logger
logger = logging.getLogger(__name__)

# Global vector store instance
_vector_store: Optional[Neo4jVector] = None

def get_vector_store(embeddings: Optional[Embeddings] = None) -> Neo4jVector:
    """Get or create a Neo4j vector store instance"""
    global _vector_store
    
    if _vector_store is None:
        try:
            # Use provided embeddings or get default
            if embeddings is None:
                embeddings = get_embeddings()
            
            logger.info("Initializing Neo4j vector store")
            
            # Set up vector store
            _vector_store = Neo4jVector.from_existing_graph(
                embedding=embeddings,
                url=settings.NEO4J_URI,
                username=settings.NEO4J_USERNAME,
                password=settings.NEO4J_PASSWORD,
                database=settings.NEO4J_DATABASE,
                node_label="NavigationNode",
                text_node_properties=["title", "url"],
                embedding_node_property="embedding",
                index_name="navigation_vector_index",
            )
            
            logger.info("Neo4j vector store initialized successfully")
        
        except Exception as e:
            logger.error(f"Failed to initialize Neo4j vector store: {str(e)}")
            raise
    
    return _vector_store

def create_vector_index() -> None:
    """Create vector index in Neo4j for navigation nodes"""
    try:
        # Get vector store (this will create the index if it doesn't exist)
        get_vector_store()
        
        # Create Cypher query to set up vector index
        query = """
        CALL db.index.vector.createNodeIndex(
          'navigation_vector_index',
          'NavigationNode',
          'embedding',
          1536,
          'cosine'
        )
        """
        
        # Execute the query using the Neo4j driver directly
        from app.database.neo4j import execute_query
        execute_query(query)
        
        logger.info("Vector index created successfully")
    
    except Exception as e:
        logger.error(f"Error creating vector index: {str(e)}")
        # Handle the case where the index already exists
        if "already exists" in str(e):
            logger.info("Vector index already exists")
        else:
            raise

def update_node_embeddings() -> None:
    """Update embeddings for all navigation nodes in Neo4j"""
    try:
        # Get embeddings model
        embeddings = get_embeddings()
        
        # Get all nodes from Neo4j
        from app.database.neo4j import execute_query
        query = """
        MATCH (n:NavigationNode)
        RETURN n.id as id, n.title as title, n.url as url
        """
        nodes = execute_query(query)
        
        logger.info(f"Found {len(nodes)} nodes to update embeddings for")
        
        # Update embeddings for each node
        for node in nodes:
            # Create text to embed (combine title and URL)
            text = f"{node['title']} {node['url']}"
            
            # Generate embedding
            embedding = embeddings.embed_query(text)
            
            # Update node with embedding
            update_query = """
            MATCH (n:NavigationNode {id: $id})
            SET n.embedding = $embedding
            """
            
            params = {
                "id": node["id"],
                "embedding": embedding
            }
            
            execute_query(update_query, params)
            logger.info(f"Updated embedding for node: {node['id']}")
        
        logger.info("All node embeddings updated successfully")
    
    except Exception as e:
        logger.error(f"Error updating node embeddings: {str(e)}")
        raise

def retrieve_similar_nodes(query: str, k: int = 5) -> List[Dict[str, Any]]:
    """Retrieve nodes similar to the query using vector search"""
    try:
        # Get vector store
        vector_store = get_vector_store()
        
        # Search for similar nodes
        logger.info(f"Retrieving nodes similar to query: {query}")
        documents = vector_store.similarity_search(query, k=k)
        
        # Convert documents to dictionaries
        results = []
        for doc in documents:
            # Extract metadata and page content
            meta = doc.metadata
            content = doc.page_content
            
            # Create result dictionary
            result = {
                "id": meta.get("id", ""),
                "title": meta.get("title", ""),
                "url": meta.get("url", ""),
                "content": content,
                "score": meta.get("score", 0.0)
            }
            
            results.append(result)
        
        logger.info(f"Retrieved {len(results)} similar nodes")
        return results
    
    except Exception as e:
        logger.error(f"Error retrieving similar nodes: {str(e)}")
        return []

def initialize_vector_search() -> None:
    """Initialize vector search by creating index and updating embeddings"""
    try:
        # Create vector index
        create_vector_index()
        
        # Update embeddings for all nodes
        update_node_embeddings()
        
        logger.info("Vector search initialized successfully")
    
    except Exception as e:
        logger.error(f"Error initializing vector search: {str(e)}")
        raise 