from pydantic import BaseModel, Field
from typing import Optional

from datetime import datetime

from bson import ObjectId

class Deepfake(BaseModel):
    deepfake_id: Optional[str] = Field(default_factory=lambda: str(ObjectId()))
    source_uri: str
    target_uri: str
    output_uri: Optional[str] = ""
    status: Optional[str] = "in progress"
    keep_fps: bool
    enhance_face: bool
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    user_id: str