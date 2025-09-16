import json
import os
from datetime import datetime
from typing import Dict, Any

def log_event(event_type: str, data: Dict[str, Any]) -> None:
    """
    Log an event to a JSON file for auditing purposes.
    
    Args:
        event_type: Type of event (e.g., 'scan', 'analysis', 'error')
        data: Dictionary containing event data
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "data": data
    }
    
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Append to log file
    log_file = os.path.join(logs_dir, "events.log")
    
    try:
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"Failed to log event: {e}")

def get_recent_events(limit: int = 100) -> list:
    """
    Retrieve recent events from the log file.
    
    Args:
        limit: Maximum number of events to return
        
    Returns:
        List of recent events
    """
    log_file = os.path.join("logs", "events.log")
    
    if not os.path.exists(log_file):
        return []
    
    events = []
    try:
        with open(log_file, "r") as f:
            lines = f.readlines()
            
        # Get the last 'limit' lines
        recent_lines = lines[-limit:] if len(lines) > limit else lines
        
        for line in recent_lines:
            try:
                event = json.loads(line.strip())
                events.append(event)
            except json.JSONDecodeError:
                continue
                
    except Exception as e:
        print(f"Failed to read events: {e}")
    
    return events
