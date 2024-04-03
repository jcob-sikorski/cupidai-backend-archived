from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

class Prompt(BaseModel):
    prompt: str
    generation_speed: Optional[str]
    engine_version: Optional[str]
    style: Optional[str]
    aspect_ratio: Optional[str]
    step_stop: Optional[str]
    stylize: Optional[str]
    seed: Optional[str]

class Progress(BaseModel):
    messageId: str = Field(..., alias="messageId")
    prompt: str
    uri: Optional[str]
    progress: Optional[int]
    createdAt: str = Field(..., alias="createdAt")
    updatedAt: str = Field(..., alias="updatedAt")
    buttons: Optional[List[str]]
    originatingMessageId: Optional[str] = Field(..., alias="originatingMessageId")
    ref: Optional[str]

class ImagineResponse(BaseModel):
    success: bool
    messageId: str
    createdAt: str
    error: Optional[str]