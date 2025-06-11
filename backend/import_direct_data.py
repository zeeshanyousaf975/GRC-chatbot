import logging
import sys
import os
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Add the current directory to the path to import app modules
sys.path.insert(0, os.path.abspath("."))

try:
    from app.database.neo4j import get_neo4j_driver, create_graph_constraints_and_indexes, execute_query
    from app.langchain.retriever import initialize_vector_search
    
    def import_direct_data():
        """Import sample navigation data directly into Neo4j"""
        try:
            logger.info("Connecting to Neo4j database")
            get_neo4j_driver()
            
            logger.info("Creating constraints and indexes")
            create_graph_constraints_and_indexes()
            
            # Define sample nodes - these match some of the structure in sampleMindMap.ts
            nodes = [
                {
                    "id": "root", 
                    "title": "Software Navigation", 
                    "url": "https://staging.zazoon.com/dashboard",
                    "properties": {}
                },
                {
                    "id": "solutions", 
                    "title": "SOLUTIONS", 
                    "url": "https://staging.zazoon.com/solutions",
                    "properties": {"isExpandable": True}
                },
                {
                    "id": "information_security", 
                    "title": "Information Security", 
                    "url": "https://staging.zazoon.com/solutions/ism",
                    "properties": {"isExpandable": True}
                },
                {
                    "id": "frameworks", 
                    "title": "Frameworks", 
                    "url": "https://staging.zazoon.com/solutions/ism/frameworks",
                    "properties": {
                        "context": "information security",
                        "parentSection": "Information Security",
                        "isExpandable": True
                    }
                },
                {
                    "id": "data_protection", 
                    "title": "Data Protection", 
                    "url": "https://staging.zazoon.com/solutions/data-protection",
                    "properties": {"isExpandable": True}
                },
                {
                    "id": "business_continuity", 
                    "title": "Business Continuity", 
                    "url": "https://staging.zazoon.com/solutions/business-continuity",
                    "properties": {"isExpandable": True}
                }
            ]
            
            # Import nodes
            logger.info("Importing nodes")
            for node in nodes:
                query = """
                MERGE (n:NavigationNode {id: $id})
                SET n.title = $title,
                    n.url = $url,
                    n.properties = $properties
                """
                
                params = {
                    "id": node["id"],
                    "title": node["title"],
                    "url": node["url"],
                    "properties": json.dumps(node["properties"])
                }
                
                execute_query(query, params)
                logger.info(f"Created/updated node: {node['id']}")
            
            # Define relationships
            relationships = [
                {"source": "root", "target": "solutions"},
                {"source": "solutions", "target": "information_security"},
                {"source": "solutions", "target": "data_protection"},
                {"source": "solutions", "target": "business_continuity"},
                {"source": "information_security", "target": "frameworks"}
            ]
            
            # Import relationships
            logger.info("Importing relationships")
            for rel in relationships:
                query = """
                MATCH (source:NavigationNode {id: $source_id})
                MATCH (target:NavigationNode {id: $target_id})
                MERGE (source)-[r:CONTAINS]->(target)
                """
                
                params = {
                    "source_id": rel["source"],
                    "target_id": rel["target"]
                }
                
                execute_query(query, params)
                logger.info(f"Created relationship: {rel['source']} -> {rel['target']}")
            
            # Initialize vector search
            logger.info("Initializing vector search")
            initialize_vector_search()
            
            logger.info("Sample data import completed successfully")
        
        except Exception as e:
            logger.error(f"Error importing sample data: {e}")
            raise

    if __name__ == "__main__":
        import_direct_data()

except ImportError as e:
    logger.error(f"Error importing required modules: {str(e)}")
    sys.exit(1) 