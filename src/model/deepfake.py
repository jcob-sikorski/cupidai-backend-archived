from pydantic import BaseModel, Field
from typing import Optional, Dict, List

from datetime import datetime

class Message(BaseModel):
    user_id: str
    status: Optional[str] = None
    uploadcare_uris: Optional[List[str]] = None # the last one is the target uri
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    message_id: Optional[str] = None
    reference_face_distance: Optional[float] = None
    face_enhancer_model: Optional[str] = None
    frame_enhancer_blend: Optional[float] = None
    s3_uris: Optional[List[str]] = None