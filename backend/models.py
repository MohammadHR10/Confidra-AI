from pydantic import BaseModel
from typing import Optional, Dict, Any

class AskRequest(BaseModel):
    query: str
    user_id: str

class AskResponse(BaseModel):
    action: str  # "pass", "blocked", "redacted"
    reason: str
    safe_output: str
    evidence: Optional[Dict[str, Any]] = {}
