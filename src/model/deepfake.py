from pydantic import BaseModel, Field
from typing import Optional, List

from datetime import datetime

class Message(BaseModel):
    user_id: str
    status: Optional[str] = None
    source_uri: Optional[str] = None
    target_uri: Optional[str] = None
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    message_id: Optional[str] = None
    s3_uri: Optional[str] = None