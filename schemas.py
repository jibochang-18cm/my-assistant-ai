from typing import List, Dict, Optional
from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str
    history: Optional[List[Dict[str, str]]] = []
