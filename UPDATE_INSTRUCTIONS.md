# Dependency Update Instructions

## Overview

This document provides instructions on updating the Navigation Chatbot application to use the latest compatible dependencies. The updates include:

1. Updated backend dependencies (FastAPI, LangChain, Neo4j, etc.)
2. Updated frontend dependencies (React, Axios, react-markdown, etc.)
3. Updated Docker images (Python, Node.js, Neo4j)
4. Code adjustments for compatibility

## Update Process

### 1. Update Backend Dependencies

1. Update `requirements.txt` with the latest versions:

```bash
# FastAPI and server
fastapi>=0.110.0
uvicorn>=0.27.1
python-dotenv>=1.0.1
pydantic>=2.6.3

# LangChain and LLM
langchain>=0.1.13
langchain-core>=0.1.22
langchain-groq>=0.1.5
groq>=0.9.0

# Neo4j
neo4j>=5.16.0
langchain-neo4j>=0.1.3

# Vector embeddings
sentence-transformers>=2.5.1

# Utilities
numpy>=1.26.4
python-multipart>=0.0.9
typing-extensions>=4.10.0
```

2. Install the updated dependencies:

```bash
cd backend
pip install -r requirements.txt
```

### 2. Update Frontend Dependencies

1. Update `package.json` with the latest versions:

```json
"dependencies": {
  "@testing-library/jest-dom": "^6.1.5",
  "@testing-library/react": "^14.1.2",
  "@testing-library/user-event": "^14.5.1",
  "axios": "^1.6.2",
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-markdown": "^9.0.1",
  "react-scripts": "5.0.1",
  "web-vitals": "^3.5.0"
}
```

2. Install the updated dependencies:

```bash
cd frontend
npm install
```

### 3. Code Adjustments

The following files have been updated for compatibility with the newer dependencies:

#### Backend

1. `app/langchain/llm.py`
   - Updated imports from `langchain` to `langchain_core`
   - Updated callback handling for streaming responses

2. `app/langchain/embeddings.py`
   - Updated import from `langchain.embeddings` to `langchain_community.embeddings`

3. `app/langchain/retriever.py`
   - Updated imports from `langchain` to `langchain_core`
   - Changed parameter name from `embeddings` to `embedding` in Neo4jVector initialization

4. `app/langchain/chains.py`
   - Updated imports from `langchain` to `langchain_core` where appropriate
   - Updated chain creation with new API pattern using `create_retrieval_chain`

#### Frontend

The `ChatInterface.jsx` component should work with the updated react-markdown v9 without changes.

### 4. Docker Configuration Updates

1. Updated Docker base images:
   - Backend: Python 3.12 (from 3.10)
   - Frontend: Node.js 20 (from 18)
   - Neo4j: 5.18.0 (from 5.14.0)

### 5. Deployment Steps

1. Build and start the updated containers:

```bash
docker-compose build --no-cache
docker-compose up -d
```

2. Check for any runtime errors:

```bash
docker-compose logs -f
```

## Testing

After updating, test the following functionality:

1. **Frontend-Backend Communication**: Ensure the chat interface can send messages to the backend and receive responses.

2. **Neo4j Vector Search**: Verify that the vector search functionality works with the updated Neo4j and LangChain versions.

3. **GROQ LLM Integration**: Confirm that the GROQ API integration functions correctly with the updated LangChain version.

4. **Markdown Rendering**: Test that markdown content renders correctly with the updated react-markdown.

## Troubleshooting

If you encounter issues after updating:

1. **LangChain Import Errors**: Check for any additional import changes in the LangChain library.

2. **Neo4j Connection Issues**: Verify that the Neo4j connection parameters match the updated Neo4j version.

3. **React Markdown Rendering Issues**: If markdown doesn't render correctly, check the react-markdown documentation for v9 API changes.

4. **Container Build Failures**: Check the Docker build logs for any dependency conflicts or installation errors. 