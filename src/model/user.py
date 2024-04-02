from uuid import UUID
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    name: str
    hash: str
    id: Optional[UUID] = None

