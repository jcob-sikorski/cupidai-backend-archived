from typing import Dict
from pydantic import BaseModel, UUID4

class DeepfakeStatus(BaseModel):
    status: str
    progress: int

class DeepfakeUsage(BaseModel):
    generated_num: int

class Deepfake(BaseModel):
    source_uri: str
    target_uri: str
    face_to_swap: str
    max_face_simplicity: float
    post_processor: str
    image_blend_ratio: float
