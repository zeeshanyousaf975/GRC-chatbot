import json
import logging
import os
from typing import Dict, Any, List, Optional

from app.database.neo4j import execute_query

# Configure logger
logger = logging.getLogger(__name__)

def parse_ts_to_json(ts_file_path: str) -> Dict[str, Any]:
    """
    Parse TypeScript file with mindmap data to JSON.
    This is a simplified parser that expects a specific format.
    """
    try:
        with open(ts_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Extract JSON part from TS file
        # Find the object declaration
        start_idx = content.find('export const sampleMindMap')
        if start_idx == -1:
            raise ValueError("Could not find sampleMindMap declaration in the file")
        
        # Find the object content starting point
        start_idx = content.find('{', start_idx)
        if start_idx == -1:
            raise ValueError("Could not find the start of the object in the file")
        
        # Find the end of the object
        # This is a simplistic approach that assumes proper formatting
        braces_count = 0
        end_idx = start_idx
        
        for i in range(start_idx, len(content)):
            if content[i] == '{':
                braces_count += 1
            elif content[i] == '}':
                braces_count -= 1
                if braces_count == 0:
                    end_idx = i + 1
                    break
        
        if end_idx <= start_idx:
            raise ValueError("Could not find the end of the object in the file")
        
        # Extract the JSON part
        json_str = content[start_idx:end_idx]
        
        # Convert TS syntax to valid JSON
        # Remove trailing commas
        json_str = json_str.replace(',\n', ',')
        json_str = json_str.replace(',]', ']')
        json_str = json_str.replace(',}', '}')
        
        # Parse the JSON
        mindmap_data = json.loads(json_str)
        return mindmap_data
        
    except Exception as e:
        logger.error(f"Error parsing TypeScript file: {str(e)}")
        raise

def process_node(node: Dict[str, Any], parent_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Process a node and its children, returning a list of nodes and relationships"""
    results = []
    
    # Create node data
    node_data = {
        "id": node["id"],
        "title": node["title"],
        "url": node.get("url", ""),
        "properties": {k: v for k, v in node.items() if k not in ["id", "title", "url", "children"]}
    }
    
    # Add node to results
    results.append({
        "type": "node",
        "data": node_data
    })
    
    # Create relationship to parent if exists
    if parent_id:
        results.append({
            "type": "relationship",
            "data": {
                "source_id": parent_id,
                "target_id": node["id"],
                "type": "CONTAINS"
            }
        })
    
    # Process children
    if "children" in node and node["children"]:
        for child in node["children"]:
            child_results = process_node(child, node["id"])
            results.extend(child_results)
    
    return results

def import_mindmap_to_neo4j(mindmap_data: Dict[str, Any]) -> None:
    """Import mindmap data to Neo4j"""
    try:
        # Process the root node and all children
        root_node = mindmap_data["rootNode"]
        processed_data = process_node(root_node)
        
        # Import nodes
        nodes = [item["data"] for item in processed_data if item["type"] == "node"]
        for node in nodes:
            # Convert properties to JSON string
            properties_json = json.dumps(node["properties"])
            
            # Create node query
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
                "properties": properties_json
            }
            
            # Execute query
            execute_query(query, params)
            logger.info(f"Created/updated node: {node['id']}")
        
        # Import relationships
        relationships = [item["data"] for item in processed_data if item["type"] == "relationship"]
        for rel in relationships:
            query = """
            MATCH (source:NavigationNode {id: $source_id})
            MATCH (target:NavigationNode {id: $target_id})
            MERGE (source)-[r:CONTAINS]->(target)
            """
            
            params = {
                "source_id": rel["source_id"],
                "target_id": rel["target_id"]
            }
            
            # Execute query
            execute_query(query, params)
            logger.info(f"Created relationship: {rel['source_id']} -> {rel['target_id']}")
        
        logger.info(f"Successfully imported mindmap with {len(nodes)} nodes and {len(relationships)} relationships")
    
    except Exception as e:
        logger.error(f"Error importing mindmap to Neo4j: {str(e)}")
        raise

def import_mindmap_from_file(file_path: str) -> None:
    """Import mindmap from a TypeScript file to Neo4j"""
    try:
        # Parse TS file to JSON
        mindmap_data = parse_ts_to_json(file_path)
        
        # Import to Neo4j
        import_mindmap_to_neo4j(mindmap_data)
        
        logger.info(f"Successfully imported mindmap from {file_path}")
    
    except Exception as e:
        logger.error(f"Error importing mindmap from file: {str(e)}")
        raise

if __name__ == "__main__":
    # For testing the module directly
    import sys
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        import_mindmap_from_file(file_path)
    else:
        print("Please provide the path to the mindmap TypeScript file") 