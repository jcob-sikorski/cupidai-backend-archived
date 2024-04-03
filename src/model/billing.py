from pydantic import BaseModel
from typing import List

class Plan(BaseModel):
    name: str
    features: List[str]

class UserPlan(BaseModel):
    user_id: str
    name: str