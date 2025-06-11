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
    
    def import_comprehensive_data():
        """Import more comprehensive navigation data directly into Neo4j"""
        try:
            # First, clear the existing data
            logger.info("Clearing existing navigation data")
            clear_query = """
            MATCH (n:NavigationNode)
            DETACH DELETE n
            """
            execute_query(clear_query)
            logger.info("Existing navigation data cleared")
            
            # Connect to Neo4j
            logger.info("Connecting to Neo4j database")
            get_neo4j_driver()
            
            logger.info("Creating constraints and indexes")
            create_graph_constraints_and_indexes()
            
            # Define a more comprehensive set of nodes
            nodes = [
                # Main navigation
                {"id": "root", "title": "Software Navigation", "url": "https://staging.zazoon.com/dashboard", "properties": {}},
                {"id": "solutions", "title": "SOLUTIONS", "url": "https://staging.zazoon.com/solutions", "properties": {"isExpandable": True}},
                
                # Information Security section
                {"id": "information_security", "title": "Information Security", "url": "https://staging.zazoon.com/solutions/ism", "properties": {"isExpandable": True}},
                {"id": "is_frameworks", "title": "Frameworks", "url": "https://staging.zazoon.com/solutions/ism/frameworks", "properties": {"context": "information security", "parentSection": "Information Security", "isExpandable": True}},
                {"id": "is_item_mappings", "title": "Item Mappings", "url": "https://staging.zazoon.com/solutions/ism/item-mappings", "properties": {"context": "information security", "parentSection": "Information Security", "isExpandable": True}},
                {"id": "is_solution_features", "title": "Solution Features", "url": "https://staging.zazoon.com/solutions/ism/features", "properties": {"context": "information security", "parentSection": "Information Security", "isExpandable": True}},
                {"id": "is_template_library", "title": "Template Library", "url": "https://staging.zazoon.com/solutions/ism/templates", "properties": {"context": "information security", "parentSection": "Information Security", "isExpandable": True}},
                
                # Data Protection section
                {"id": "data_protection", "title": "Data Protection", "url": "https://staging.zazoon.com/solutions/data-protection", "properties": {"isExpandable": True}},
                {"id": "dp_frameworks", "title": "Frameworks", "url": "https://staging.zazoon.com/solutions/data-protection/frameworks", "properties": {"context": "data protection", "parentSection": "Data Protection", "isExpandable": True}},
                {"id": "dp_item_mappings", "title": "Item Mappings", "url": "https://staging.zazoon.com/solutions/data-protection/item-mappings", "properties": {"context": "data protection", "parentSection": "Data Protection", "isExpandable": True}},
                {"id": "dp_solution_features", "title": "Solution Features", "url": "https://staging.zazoon.com/solutions/data-protection/features", "properties": {"context": "data protection", "parentSection": "Data Protection", "isExpandable": True}},
                {"id": "dp_template_library", "title": "Template Library", "url": "https://staging.zazoon.com/solutions/data-protection/templates", "properties": {"context": "data protection", "parentSection": "Data Protection", "isExpandable": True}},
                
                # Business Continuity section
                {"id": "business_continuity", "title": "Business Continuity", "url": "https://staging.zazoon.com/solutions/business-continuity", "properties": {"isExpandable": True}},
                {"id": "bc_frameworks", "title": "Frameworks", "url": "https://staging.zazoon.com/solutions/business-continuity/frameworks", "properties": {"context": "business continuity", "parentSection": "Business Continuity", "isExpandable": True}},
                {"id": "bc_item_mappings", "title": "Item Mappings", "url": "https://staging.zazoon.com/solutions/business-continuity/item-mappings", "properties": {"context": "business continuity", "parentSection": "Business Continuity", "isExpandable": True}},
                {"id": "bc_solution_features", "title": "Solution Features", "url": "https://staging.zazoon.com/solutions/business-continuity/features", "properties": {"context": "business continuity", "parentSection": "Business Continuity", "isExpandable": True}},
                {"id": "bc_template_library", "title": "Template Library", "url": "https://staging.zazoon.com/solutions/business-continuity/templates", "properties": {"context": "business continuity", "parentSection": "Business Continuity", "isExpandable": True}},
                
                # Framework examples
                {"id": "iso_9001_2015", "title": "ISO 9001:2015", "url": "https://staging.zazoon.com/solutions/ism/frameworks/iso-9001-2015", "properties": {"context": "information security", "parentSection": "Frameworks", "hasAssessment": True}},
                {"id": "iso_27001", "title": "ISO 27001", "url": "https://staging.zazoon.com/solutions/ism/frameworks/iso-27001", "properties": {"context": "information security", "parentSection": "Frameworks", "hasAssessment": True}},
                {"id": "gdpr", "title": "GDPR", "url": "https://staging.zazoon.com/solutions/data-protection/frameworks/gdpr", "properties": {"context": "data protection", "parentSection": "Frameworks", "hasAssessment": True}},
                
                # Features
                {"id": "risk_management", "title": "Risk Management", "url": "https://staging.zazoon.com/solutions/ism/features/risk-management", "properties": {"context": "information security", "parentSection": "Solution Features"}},
                {"id": "process_modelling", "title": "Process Modelling", "url": "https://staging.zazoon.com/solutions/data-protection/features/process-modelling", "properties": {"context": "data protection", "parentSection": "Solution Features"}},
                {"id": "dora", "title": "Digital Operational Resilience Act (DORA)", "url": "https://staging.zazoon.com/solutions/data-protection/features/dora", "properties": {"context": "data protection", "parentSection": "Solution Features"}}
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
                # Main structure
                {"source": "root", "target": "solutions"},
                {"source": "solutions", "target": "information_security"},
                {"source": "solutions", "target": "data_protection"},
                {"source": "solutions", "target": "business_continuity"},
                
                # Information Security children
                {"source": "information_security", "target": "is_frameworks"},
                {"source": "information_security", "target": "is_item_mappings"},
                {"source": "information_security", "target": "is_solution_features"},
                {"source": "information_security", "target": "is_template_library"},
                
                # Data Protection children
                {"source": "data_protection", "target": "dp_frameworks"},
                {"source": "data_protection", "target": "dp_item_mappings"},
                {"source": "data_protection", "target": "dp_solution_features"},
                {"source": "data_protection", "target": "dp_template_library"},
                
                # Business Continuity children
                {"source": "business_continuity", "target": "bc_frameworks"},
                {"source": "business_continuity", "target": "bc_item_mappings"},
                {"source": "business_continuity", "target": "bc_solution_features"},
                {"source": "business_continuity", "target": "bc_template_library"},
                
                # Frameworks
                {"source": "is_frameworks", "target": "iso_9001_2015"},
                {"source": "is_frameworks", "target": "iso_27001"},
                {"source": "dp_frameworks", "target": "gdpr"},
                
                # Features
                {"source": "is_solution_features", "target": "risk_management"},
                {"source": "dp_solution_features", "target": "process_modelling"},
                {"source": "dp_solution_features", "target": "dora"}
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
            
            logger.info("Comprehensive data import completed successfully")
        
        except Exception as e:
            logger.error(f"Error importing comprehensive data: {e}")
            raise

    if __name__ == "__main__":
        import_comprehensive_data()

except ImportError as e:
    logger.error(f"Error importing required modules: {str(e)}")
    sys.exit(1) 