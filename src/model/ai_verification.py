from pydantic import BaseModel
from typing import Optional


# TODO: add quality parameter in v2

# TODO: add social_account_id because each social account is associated with the prompt

class Prompt(BaseModel):
    prompt: str # ✅
    account_id: str
    # generation_speed: Optional[str]
    version: Optional[str] # ✅ 1.
    style: Optional[str] # ✅ 1.
    aspect: Optional[str] # ✅ 1.
    stop: Optional[str] # ✅ 1.
    stylize: Optional[str] # ✅ 1.
    seed: Optional[str] # ✅ 1.
    user_id: str | None = None

# Note: 1. means tested as one parameter without others
