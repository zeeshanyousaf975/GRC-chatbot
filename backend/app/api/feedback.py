import logging
from typing import Dict, Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Configure logger
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Feedback request model
class FeedbackRequest(BaseModel):
    query: str
    response: str
    helpful: bool
    comment: Optional[str] = None
    selected_node_id: Optional[str] = None

# Feedback response model
class FeedbackResponse(BaseModel):
    status: str
    message: str

@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest) -> Dict[str, str]:
    """
    Submit user feedback on a navigation response
    """
    try:
        # Validate feedback
        if not request.query or len(request.query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        if not request.response or len(request.response.strip()) == 0:
            raise HTTPException(status_code=400, detail="Response cannot be empty")
        
        # Log feedback
        logger.info(f"Received feedback for query: {request.query}")
        logger.info(f"Feedback: helpful={request.helpful}, selected_node={request.selected_node_id}")
        
        if request.comment:
            logger.info(f"Comment: {request.comment}")
        
        # Here you would typically store the feedback in a database
        # For now, we just log it
        
        return {
            "status": "success",
            "message": "Feedback submitted successfully"
        }
    
    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error submitting feedback: {str(e)}") 