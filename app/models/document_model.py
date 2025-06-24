from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Document(BaseModel):
    url: str
    raw_text: str
    clean_text: str
    vector_id: Optional[str] = None
    timestamp: datetime = datetime.utcnow()