from pydantic import BaseModel
from typing import Optional

class Prompt(BaseModel):
    prompt: str
    generation_speed: Optional[str]
    engine_version: Optional[str]
    style: Optional[str]
    aspect_ratio: Optional[str]
    step_stop: Optional[str]
    stylize: Optional[str]
    seed: Optional[str]