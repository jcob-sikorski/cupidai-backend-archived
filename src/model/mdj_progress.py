from pydantic import BaseModel, Field
from typing import List, Optional

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