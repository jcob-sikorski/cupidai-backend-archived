from pydantic import BaseModel
from typing import List

class Team(BaseModel):
    members: List[str]
    name: str
    owner: str

class Member:
    user_id: str
    permissions: List[str]