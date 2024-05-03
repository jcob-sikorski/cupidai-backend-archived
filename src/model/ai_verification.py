from pydantic import BaseModel
from typing import Optional


# TODO: add quality parameter in v2

class Prompt(BaseModel):
    prompt: str # ✅
    # generation_speed: Optional[str]
    version: Optional[str] # ✅ 1.
    style: Optional[str] # ✅ 1.
    aspect: Optional[str] # ✅ 1.
    stop: Optional[str] # ✅ 1.
    stylize: Optional[str] # ✅ 1.
    seed: Optional[str] # ✅ 1.

# Note: 1. means tested as one parameter without others
