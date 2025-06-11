import logging
from typing import Optional

from neo4j import Driver, GraphDatabase
from app.core.config import settings

# Configure logger
logger = logging.getLogger(__name__)

# Global driver instance
_driver: Optional[Driver] = None

def get_neo4j_driver() -> Driver:
    """Get or create a Neo4j driver instance"""
    global _driver
    
    if _driver is None:
        try:
            # Create a new driver instance
            logger.info(f"Connecting to Neo4j database at {settings.NEO4J_URI}")
            
            # Configure authentication
            auth = (settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)
            
            # Create driver
            _driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=auth,
                database=settings.NEO4J_DATABASE
            )
            
            # Verify connectivity
            _driver.verify_connectivity()
            logger.info("Successfully connected to Neo4j database")
            
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j database: {str(e)}")
            raise
    
    return _driver

def close_neo4j_driver() -> None:
    """Close the Neo4j driver instance"""
    global _driver
    
    if _driver is not None:
        logger.info("Closing Neo4j driver")
        try:
            _driver.close()
            _driver = None
            logger.info("Neo4j driver closed successfully")
        except Exception as e:
            logger.error(f"Error closing Neo4j driver: {str(e)}")
            raise

def execute_query(query: str, params: dict = None) -> list:
    """Execute a Cypher query on the Neo4j database"""
    driver = get_neo4j_driver()
    
    with driver.session() as session:
        result = session.run(query, params)
        return [record.data() for record in result]

def create_graph_constraints_and_indexes() -> None:
    """Create constraints and indexes for the graph database"""
    # Define constraints and indexes for navigation nodes
    constraints = [
        "CREATE CONSTRAINT IF NOT EXISTS FOR (n:NavigationNode) REQUIRE n.id IS UNIQUE",
        "CREATE INDEX IF NOT EXISTS FOR (n:NavigationNode) ON (n.title)",
        "CREATE INDEX IF NOT EXISTS FOR (n:NavigationNode) ON (n.url)",
    ]
    
    # Execute each constraint/index query
    for constraint in constraints:
        try:
            execute_query(constraint)
            logger.info(f"Successfully executed: {constraint}")
        except Exception as e:
            logger.error(f"Failed to execute constraint: {constraint}")
            logger.error(f"Error: {str(e)}")

# Initialize constraints and indexes when module is imported
try:
    # Only initialize when not imported for testing
    if __name__ != "__main__":
        create_graph_constraints_and_indexes()
except Exception as e:
    logger.error(f"Error initializing database: {str(e)}") 