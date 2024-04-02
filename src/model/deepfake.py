from pydantic import BaseModel
from typing import Optional

class DeepfakeStatus(BaseModel):
    output_uri: str
    status: str

class DeepfakeUsage(BaseModel):
    user_id: str
    generated_num: int

class Deepfake(BaseModel):
    source_uri: str
    target_uri: str
    keep_fps: bool
    enhance_face: bool
