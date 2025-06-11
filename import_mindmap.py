import logging
import sys
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Add the current directory to the path to import app modules
sys.path.insert(0, os.path.abspath("."))

try:
    from app.database.neo4j import get_neo4j_driver, create_graph_constraints_and_indexes
    from app.database.mindmap import import_mindmap_from_file
    from app.langchain.retriever import initialize_vector_search
    
    # Main function
    def import_mindmap():
        try:
            # Get absolute path to the mindmap file
            mindmap_file = os.path.abspath("../sampleMindMap.ts")
            
            # Check if the file exists
            if not os.path.isfile(mindmap_file):
                logger.error(f"Mindmap file not found: {mindmap_file}")
                sys.exit(1)
            
            # Connect to Neo4j and create constraints
            logger.info("Connecting to Neo4j database")
            get_neo4j_driver()
            
            # Create constraints and indexes
            logger.info("Creating constraints and indexes")
            create_graph_constraints_and_indexes()
            
            # Import mindmap data
            logger.info(f"Importing mindmap from {mindmap_file}")
            import_mindmap_from_file(mindmap_file)
            
            # Initialize vector search
            logger.info("Initializing vector search")
            initialize_vector_search()
            
            logger.info("Mindmap import completed successfully")
        
        except Exception as e:
            logger.error(f"Error importing mindmap: {str(e)}")
            raise

    # Run the import function
    if __name__ == "__main__":
        import_mindmap()

except ImportError as e:
    logger.error(f"Error importing required modules: {str(e)}")
    sys.exit(1) 