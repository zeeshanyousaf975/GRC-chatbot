#!/usr/bin/env python
"""
Script to set up Neo4j database for the navigation chatbot
"""

import os
import sys
import logging
import argparse
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database.neo4j import get_neo4j_driver, create_graph_constraints_and_indexes
from app.database.mindmap import import_mindmap_from_file
from app.langchain.retriever import initialize_vector_search

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def setup_database(mindmap_file: str) -> None:
    """Set up Neo4j database and import mindmap data"""
    try:
        # Get Neo4j driver to ensure connection
        logger.info("Connecting to Neo4j database")
        get_neo4j_driver()
        
        # Create constraints and indexes
        logger.info("Creating constraints and indexes")
        create_graph_constraints_and_indexes()
        
        # Import mindmap data
        logger.info(f"Importing mindmap data from {mindmap_file}")
        import_mindmap_from_file(mindmap_file)
        
        # Initialize vector search
        logger.info("Initializing vector search")
        initialize_vector_search()
        
        logger.info("Database setup completed successfully")
    
    except Exception as e:
        logger.error(f"Error setting up database: {str(e)}")
        sys.exit(1)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Set up Neo4j database for navigation chatbot")
    parser.add_argument("--mindmap", required=True, help="Path to mindmap TypeScript file")
    
    args = parser.parse_args()
    
    # Check if mindmap file exists
    if not os.path.isfile(args.mindmap):
        logger.error(f"Mindmap file not found: {args.mindmap}")
        sys.exit(1)
    
    # Set up database
    setup_database(args.mindmap)

if __name__ == "__main__":
    main() 