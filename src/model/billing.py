from pydantic import BaseModel
from uuid import UUID

class Plan(BaseModel):
    name: str
    deepfake_num: int

class UserPlan(BaseModel):
    _id: UUID
    name: str