def parse_ts_to_json(ts_file_path: str) -> Dict[str, Any]:
    """
    Parse TypeScript file with mindmap data to JSON.
    This is a more robust parser that handles TypeScript syntax.
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
        ts_str = content[start_idx:end_idx]
        
        # Convert TypeScript to valid JSON
        # Replace TypeScript syntax with valid JSON
        json_str = ts_str
        
        # Handle TypeScript specific syntax
        json_str = json_str.replace("'", '"')  # Replace single quotes with double quotes
        
        # Remove trailing commas
        json_str = json_str.replace(",\n", ",")
        json_str = json_str.replace(",]", "]")
        json_str = json_str.replace(",}", "}")
        
        # Handle boolean values
        json_str = json_str.replace("true", "true")
        json_str = json_str.replace("false", "false")
        
        # Handle property names without quotes
        import re
        # Add quotes to property names that aren't quoted
        pattern = r'([{,]\s*)([a-zA-Z0-9_]+)(\s*:)'
        json_str = re.sub(pattern, r'\1"\2"\3', json_str)
        
        # Parse the JSON
        try:
            mindmap_data = json.loads(json_str)
            return mindmap_data
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            logger.error(f"JSON string excerpt: {json_str[:500]}...")
            
            # Fallback approach - manually extract the rootNode
            # This is a very basic extractor for the structure
            from collections import defaultdict
            
            def extract_node(node_str):
                """Extract a node dictionary from a string representation"""
                result = {}
                # Extract id
                id_match = re.search(r'id:\s*[\'"]([^\'"]+)[\'"]', node_str)
                if id_match:
                    result['id'] = id_match.group(1)
                
                # Extract title
                title_match = re.search(r'title:\s*[\'"]([^\'"]+)[\'"]', node_str)
                if title_match:
                    result['title'] = title_match.group(1)
                
                # Extract url
                url_match = re.search(r'url:\s*[\'"]([^\'"]+)[\'"]', node_str)
                if url_match:
                    result['url'] = url_match.group(1)
                
                # Extract isExpandable
                expandable_match = re.search(r'isExpandable:\s*(true|false)', node_str)
                if expandable_match:
                    result['isExpandable'] = expandable_match.group(1) == 'true'
                
                # Extract children if any
                children_match = re.search(r'children:\s*\[(.*?)\]', node_str, re.DOTALL)
                if children_match:
                    children_str = children_match.group(1)
                    # Find all child objects - this is very simplistic
                    child_objects = []
                    braces_count = 0
                    start = 0
                    
                    for i, char in enumerate(children_str):
                        if char == '{':
                            if braces_count == 0:
                                start = i
                            braces_count += 1
                        elif char == '}':
                            braces_count -= 1
                            if braces_count == 0:
                                child_objects.append(children_str[start:i+1])
                    
                    result['children'] = [extract_node(child) for child in child_objects]
                
                return result
            
            # Extract rootNode
            root_match = re.search(r'rootNode:\s*({.*})', content, re.DOTALL)
            if root_match:
                root_str = root_match.group(1)
                root_node = extract_node(root_str)
                return {"rootNode": root_node}
            else:
                raise ValueError("Could not extract rootNode from TypeScript file")
        
    except Exception as e:
        logger.error(f"Error parsing TypeScript file: {str(e)}")
        raise 