# Navigation Chatbot

An AI-powered navigation assistant that helps users navigate based on natural language queries. The application uses a modern stack with React frontend, FastAPI backend, LangChain for orchestration with GROQ LLM, and Neo4j for vector storage.

## Features

- Natural language queries for navigation assistance
- Vector search capabilities for relevant context retrieval
- Interactive chat interface with markdown support
- Docker support for easy deployment
- Responsive design for various devices

## Architecture

The application consists of three main components:

1. **Frontend**: React application with TypeScript and responsive design
2. **Backend**: FastAPI server with LangChain integration
3. **Database**: Neo4j graph database with vector search capabilities

## Prerequisites

- Node.js 18+ and npm
- Python 3.10+
- Docker and Docker Compose (for containerized deployment)
- GROQ API key (for LLM access)
- Neo4j database (local or cloud)

## Installation

### Using Docker (Recommended)

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/navigation-chatbot.git
   cd navigation-chatbot
   ```

2. Create a `.env` file in the root directory with your configuration:
   ```
   GROQ_API_KEY=your_groq_api_key
   NEO4J_PASSWORD=your_secure_password
   ```

3. Build and start the containers:
   ```
   docker-compose up -d
   ```

4. Access the application at `http://localhost:3000`

### Manual Installation

#### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your configuration:
   ```
   GROQ_API_KEY=your_groq_api_key
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=your_password
   FRONTEND_URL=http://localhost:3000
   ```

5. Start the backend server:
   ```
   uvicorn app.main:app --reload
   ```

#### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Create a `.env` file with your configuration:
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

4. Start the frontend development server:
   ```
   npm start
   ```

## Usage

1. Open the application in your browser
2. Type your navigation query in the chat interface
3. The AI will respond with directions based on your query
4. You can continue the conversation to get more specific directions

## Troubleshooting

### API Connection Issues

If the frontend cannot connect to the backend:

1. Ensure the backend server is running
2. Check that CORS is properly configured in the backend
3. Verify the `REACT_APP_API_URL` is correctly set in the frontend

### Neo4j Connection Issues

If the backend cannot connect to Neo4j:

1. Check Neo4j is running and accessible
2. Verify the connection details in the `.env` file
3. Make sure the Neo4j password is correct

### LLM API Issues

If you encounter LLM-related errors:

1. Verify your GROQ API key is valid
2. Check for any rate limiting or quota issues
3. Make sure you have the required permissions for the GROQ model

## Environment Variables

### Backend

- `GROQ_API_KEY`: Your GROQ API key for LLM access
- `NEO4J_URI`: URI for connecting to Neo4j database
- `NEO4J_USERNAME`: Neo4j database username
- `NEO4J_PASSWORD`: Neo4j database password
- `FRONTEND_URL`: URL of the frontend for CORS configuration
- `LANGCHAIN_VERBOSE`: Set to 'true' for verbose LangChain logs

### Frontend

- `REACT_APP_API_URL`: URL of the backend API

## License

This project is licensed under the MIT License - see the LICENSE file for details. 