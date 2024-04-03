from pydantic import BaseModel
from typing import Optional

class Status(BaseModel):
    output_uri: Optional[str]
    status: str


class Deepfake(BaseModel):
    source_uri: str
    target_uri: str
    keep_fps: bool
    enhance_face: bool
