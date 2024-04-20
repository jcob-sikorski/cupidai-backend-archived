from pydantic import BaseModel, Field
from typing import Optional, List

from datetime import datetime

class Message(BaseModel):
    user_id: str
    status: Optional[str] = None
    source_uri: Optional[str] = None
    target_uri: Optional[str] = None
    modify_video: Optional[str] = None # if modify video is not None then we know it's a video
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    job_id: Optional[str] = None
    output_url: Optional[str] = None