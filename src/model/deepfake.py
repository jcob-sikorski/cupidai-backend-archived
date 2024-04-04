from pydantic import BaseModel
from typing import Optional

class Deepfake(BaseModel):
    source_uri: str
    target_uri: str
    output_uri: Optional[str]
    status: Optional[str]
    keep_fps: bool
    enhance_face: bool