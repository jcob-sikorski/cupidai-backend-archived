from pydantic import BaseModel

class Plan(BaseModel):
    name: str
    deepfake_num: int

class UserPlan(BaseModel):
    user_id: str
    name: str

class Usage(BaseModel):
    user_id: str
    generated_num: int