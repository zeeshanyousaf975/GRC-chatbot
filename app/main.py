# Configure CORS
allowed_origins = [
    os.getenv("FRONTEND_URL", "http://localhost:3000"),  # Default frontend URL
    "http://frontend:3000",  # Docker container name
    "http://localhost:3001",  # Additional frontend URL for current setup
] 