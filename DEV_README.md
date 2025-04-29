# Chat Agent - Development Guide

This document provides detailed instructions for developers working on the Chat Agent project.

## Development Environment Setup

### Prerequisites

- Python 3.9+
- Node.js 16+
- Groq API Key (get one from [console.groq.com](https://console.groq.com))

### Quick Environment Check

Run the environment check script to ensure your system has all required components:

```
check_env.bat
```

### Initial Setup

1. Run the setup script to create all necessary environments and install dependencies:

```
setup_dev.bat
```

2. Edit `backend\.env` and add your Groq API key:

```
GROQ_API_KEY=your_api_key_here
```

### Starting the Development Environment

Run the start_dev script to launch both backend and frontend in development mode:

```
start_dev.bat
```

This will open two command windows:
- One running the backend server on http://localhost:8000
- One running the frontend server on http://localhost:3000

## Development Workflow

### Backend Development

The backend uses FastAPI with the following structure:

- `app/api/` - API endpoints
- `app/core/` - Core application functionality
- `app/models/` - Data models
- `app/services/` - Services (Groq, Autogen)
- `app/utils/` - Utility functions

Key files:
- `app/main.py` - Application entry point
- `app/api/chat.py` - Chat API endpoints
- `app/services/llm.py` - Groq LLM integration
- `app/services/agent.py` - Autogen agent implementation

When making changes to the backend:
1. Modify the necessary files
2. The backend has hot reloading enabled, so changes should be applied automatically
3. Test your API changes using the browser app or with a tool like curl/Postman

### Frontend Development

The frontend uses React with the following structure:

- `src/components/` - React components
- `src/services/` - API service integrations
- `src/styles/` - CSS styles

Key files:
- `src/App.tsx` - Main application component
- `src/components/ChatWindow.tsx` - Main chat interface
- `src/services/api.ts` - Backend API communication

When making changes to the frontend:
1. Modify the necessary files
2. The frontend has hot reloading enabled, so changes should be applied automatically
3. View your changes in the browser at http://localhost:3000

## Testing

### Backend Testing

You can manually test the backend API using curl:

```
curl -X POST "http://localhost:8000/api/chat" -H "Content-Type: application/json" -d "{\"message\":\"Hello, how are you?\"}"
```

### Frontend Testing

The frontend can be tested directly in the browser. Open http://localhost:3000 and interact with the chat interface.

## Troubleshooting

### Backend Issues

- **"No module named 'X'"**: Activate the virtual environment or install missing package with `pip install X`
- **Groq API errors**: Check your API key is set correctly and has sufficient quota

### Frontend Issues

- **Type errors**: Run `npm install --save-dev @types/react @types/react-dom @types/node`
- **"Cannot find module 'X'"**: Run `npm install X`
- **API Connection errors**: Ensure backend is running and REACT_APP_API_URL is set correctly

## Preparing for Production

When you're ready to move from development to production:

1. Update the backend to use proper security measures:
   - Set specific CORS origins
   - Consider adding authentication
   - Set appropriate rate limits

2. Update the environment variables for production:
   - Configure deployment-specific settings

3. Consider using the Docker configuration:
   - Backend Dockerfile
   - Frontend Dockerfile
   - docker-compose.yml

4. Review and test the production build:
   - For frontend: `cd frontend && npm run build` 