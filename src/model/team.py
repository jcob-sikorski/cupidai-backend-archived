from pydantic import BaseModel
from typing import Optional, List

class Team(BaseModel):
    members: List[str]
    name: str
    owner_user_id: str

class Member:
    account_id: str
    members: List[str]