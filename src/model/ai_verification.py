from pydantic import BaseModel, Field
from typing import List, Optional

class Settings(BaseModel):
    account_pass: bool
    verification_attempts: Optional[int]
    platform_verified_on: Optional[str]
    verifier_name: Optional[str]
    note: Optional[str]

class Prompt(BaseModel):
    prompt: str
    generation_speed: Optional[str]
    engine_version: Optional[str]
    style: Optional[str]
    aspect_ratio: Optional[str]
    step_stop: Optional[str]
    stylize: Optional[str]
    seed: Optional[str]

# TODO probably we're doing global credits system but lets wait for David
class Usage(BaseModel):
    user_id: str
    generated_num: int

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

class Response(BaseModel):
    success: bool
    messageId: str
    createdAt: str
    error: Optional[str]