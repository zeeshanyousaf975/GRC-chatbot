# Navigation Chatbot Project Structure

```
navigation-chatbot/
│
├── frontend/                     # React frontend application
│   ├── public/                   # Public assets
│   ├── src/                      # Source code
│   │   ├── components/           # React components
│   │   │   ├── ChatInterface.jsx # Main chat interface
│   │   │   ├── NavLinks.jsx      # Navigation links component
│   │   │   └── ...
│   │   ├── services/             # API services
│   │   ├── App.jsx               # Main application component
│   │   └── index.jsx             # Entry point
│   ├── package.json              # Frontend dependencies
│   └── README.md                 # Frontend documentation
│
├── backend/                      # FastAPI backend application
│   ├── app/                      # Application code
│   │   ├── api/                  # API endpoints
│   │   │   ├── __init__.py       
│   │   │   ├── query.py          # Query processing endpoint
│   │   │   ├── navigate.py       # Navigation recommendations endpoint
│   │   │   └── feedback.py       # User feedback endpoint
│   │   ├── core/                 # Core application code
│   │   │   ├── __init__.py
│   │   │   ├── config.py         # Configuration settings
│   │   │   └── logging.py        # Logging setup
│   │   ├── langchain/            # LangChain integration
│   │   │   ├── __init__.py
│   │   │   ├── llm.py            # GROQ LLM setup
│   │   │   ├── chains.py         # LangChain chains
│   │   │   └── agents.py         # LangChain agents
│   │   ├── database/             # Database integration
│   │   │   ├── __init__.py
│   │   │   ├── neo4j.py          # Neo4j database connection
│   │   │   └── mindmap.py        # Mindmap data import
│   │   ├── utils/                # Utility functions
│   │   │   ├── __init__.py
│   │   │   └── helpers.py        # Helper functions
│   │   └── main.py               # Application entry point
│   ├── tests/                    # Tests
│   │   ├── __init__.py
│   │   └── test_api.py           # API tests
│   ├── requirements.txt          # Backend dependencies
│   └── README.md                 # Backend documentation
│
├── data/                         # Data files
│   └── sampleMindMap.ts          # Sample mindmap data
│
├── docker/                       # Docker configuration
│   ├── frontend.Dockerfile       # Frontend Docker configuration
│   ├── backend.Dockerfile        # Backend Docker configuration
│   └── docker-compose.yml        # Docker Compose configuration
│
├── scripts/                      # Utility scripts
│   ├── setup_neo4j.py            # Script to set up Neo4j database
│   └── import_mindmap.py         # Script to import mindmap data
│
└── README.md                     # Project documentation
```

This structure organizes our navigation chatbot project into key components:

1. **Frontend**: React-based chat interface
2. **Backend**: FastAPI application with LangChain integration
3. **Data**: Storage for sample mindmap data
4. **Docker**: Containerization configuration
5. **Scripts**: Utility scripts for setup and data import 