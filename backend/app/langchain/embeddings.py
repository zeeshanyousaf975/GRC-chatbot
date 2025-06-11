import logging
from typing import Optional, List

from langchain_community.embeddings import HuggingFaceEmbeddings
from app.core.config import settings

# Configure logger
logger = logging.getLogger(__name__)

# Global embeddings instance
_embeddings: Optional[HuggingFaceEmbeddings] = None

def get_embeddings() -> HuggingFaceEmbeddings:
    """Get or create a HuggingFace embeddings instance"""
    global _embeddings
    
    if _embeddings is None:
        try:
            logger.info(f"Initializing HuggingFace embeddings with model: {settings.EMBEDDING_MODEL}")
            _embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
            logger.info("HuggingFace embeddings initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize HuggingFace embeddings: {str(e)}")
            raise
    
    return _embeddings

def get_text_embedding(text: str) -> List[float]:
    """Get embedding for a single text"""
    try:
        embeddings = get_embeddings()
        return embeddings.embed_query(text)
    except Exception as e:
        logger.error(f"Error getting text embedding: {str(e)}")
        raise

def get_documents_embeddings(documents: List[str]) -> List[List[float]]:
    """Get embeddings for a list of documents"""
    try:
        embeddings = get_embeddings()
        return embeddings.embed_documents(documents)
    except Exception as e:
        logger.error(f"Error getting documents embeddings: {str(e)}")
        raise 