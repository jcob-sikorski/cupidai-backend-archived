from pydantic import BaseModel

class Deepfake(BaseModel):
    source_uri: str
    target_uri: str
    face_to_swap: str
    max_face_simplicity: float
    post_processor: str
    image_blend_ratio: float
