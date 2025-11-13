import xml.etree.ElementTree as ET
import sys

def validate_config(params):
    errors = []
    
    if not params.get('package') or not params['package'].strip():
        errors.append("Package name is required")
    
    if not params.get('repo') or not params['repo'].strip():
        errors.append("Repository URL is required")
    
    if not params.get('output') or not params['output'].strip():
        errors.append("Output filename is required")
    
    try:
        depth = int(params.get('depth', 1))
        if depth < 1:
            errors.append("Depth must be positive number")
    except (ValueError, TypeError):
        errors.append("Depth must be a number")
    
    try:
        test_mode = params.get('test_mode', 'false').lower()
        if test_mode not in ('true', 'false', '1', '0'):
            errors.append("Test mode must be true/false")
    except:
        errors.append("Invalid test mode")
    
    return errors

try:
    config = ET.parse('config.xml').getroot()
    params = {elem.tag: elem.text for elem in config}
    
    errors = validate_config(params)
    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    
    print("Config:")
    for k, v in params.items():
        print(f"  {k}: {v}")
        
except FileNotFoundError:
    print("Error: config.xml file not found")
    sys.exit(1)
except ET.ParseError:
    print("Error: Invalid XML format in config.xml")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
