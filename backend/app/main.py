from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from dotenv import load_dotenv

# Import API routers
from app.api import query, navigate, feedback

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Navigation Chatbot API",
    description="API for AI-powered navigation chatbot",
    version="1.0.0",
)

# Configure CORS
allowed_origins = [
    os.getenv("FRONTEND_URL", "http://localhost:3000"),  # Default frontend URL
    "http://frontend:3000",  # Docker container name
]

# Add additional origins from environment variable if set
if os.getenv("ADDITIONAL_CORS_ORIGINS"):
    allowed_origins.extend(os.getenv("ADDITIONAL_CORS_ORIGINS").split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Replace wildcard with specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(query.router, prefix="/api", tags=["query"])
app.include_router(navigate.router, prefix="/api", tags=["navigate"])
app.include_router(feedback.router, prefix="/api", tags=["feedback"])

@app.get("/", tags=["root"])
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Navigation Chatbot API is running"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True) 