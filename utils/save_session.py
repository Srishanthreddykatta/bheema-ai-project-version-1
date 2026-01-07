import json
from datetime import datetime

def save_session(session_data, filename=None):
    """Save session data to JSON file."""
    if filename is None:
        filename = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w') as f:
        json.dump(session_data, f, indent=2)
    return filename
