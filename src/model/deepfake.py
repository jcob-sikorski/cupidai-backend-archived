from pydantic import BaseModel

class DeepfakeStatus(BaseModel):
    status: str
    progress: int

class DeepfakeUsage(BaseModel):
    generated_num: int

class Deepfake(BaseModel):
    source_uri: str
    target_uri: str
    keep_fps: bool
    enhance_face: bool
