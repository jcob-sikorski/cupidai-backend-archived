from datetime import datetime
from pydantic import BaseModel

class TextToImage(BaseModel):
    prompt: str
    generation_speed: str
    engine_version: str
    style: str
    aspect_ratio: str
    step: str
    stylize: str
    seed: str

class GeneratedImage(BaseModel):
    success: bool
    message_id: str
    createdAt: datetime
