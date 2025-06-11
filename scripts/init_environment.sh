#!/bin/bash

# Script to initialize the navigation chatbot environment

echo "Initializing Navigation Chatbot environment..."

# Check if .env file exists
if [ ! -f ".env" ]; then
  echo "Creating .env file..."
  cat > .env << EOF
# Neo4j configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password

# GROQ API configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# LangChain configuration
LANGCHAIN_VERBOSE=False
EOF
  echo ".env file created. Please update it with your GROQ API key."
else
  echo ".env file already exists."
fi

# Copy sample mindmap to data directory
if [ ! -d "data" ]; then
  echo "Creating data directory..."
  mkdir -p data
fi

echo "Copying sample mindmap to data directory..."
cp sampleMindMap.ts data/

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
  echo "Docker is not installed. Please install Docker and Docker Compose before continuing."
  exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
  echo "Docker Compose is not installed. Please install Docker Compose before continuing."
  exit 1
fi

echo "Starting Docker containers..."
docker-compose up -d neo4j

echo "Waiting for Neo4j to start (30 seconds)..."
sleep 30

echo "Setting up Neo4j database..."
docker-compose run --rm backend python -m scripts.setup_neo4j --mindmap /app/data/sampleMindMap.ts

echo "Starting remaining services..."
docker-compose up -d

echo "Environment initialization complete!"
echo "Frontend is running at: http://localhost:3000"
echo "Backend API is running at: http://localhost:8000"
echo "Neo4j browser is available at: http://localhost:7474"
echo ""
echo "NOTE: Before using the chatbot, make sure to update the GROQ_API_KEY in the .env file." 