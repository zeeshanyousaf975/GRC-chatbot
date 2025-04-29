"""
Development script for running the backend in development mode.
"""
import os
import uvicorn
import shutil
from dotenv import load_dotenv

# Try to load .env file if it exists
if os.path.exists('.env'):
    load_dotenv('.env')
else:
    # If no .env file exists, check if .env-example exists and copy it
    if os.path.exists('.env-example'):
        print("No .env file found. Creating one from .env-example...")
        shutil.copy('.env-example', '.env')
        print("⚠️ Please edit the .env file and add your GROQ_API_KEY ⚠️")
        load_dotenv('.env')
    else:
        print("No .env or .env-example file found. Please create a .env file.")

# Check if GROQ_API_KEY is set
groq_api_key = os.getenv('GROQ_API_KEY')
if not groq_api_key or groq_api_key == 'your_groq_api_key_here':
    print("⚠️ Warning: GROQ_API_KEY is not set or is using the default value.")
    print("⚠️ The application may not work correctly without a valid API key.")
    print("⚠️ Please edit your .env file and set a valid GROQ_API_KEY.")

if __name__ == "__main__":
    print("Starting backend development server...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug",
    ) 