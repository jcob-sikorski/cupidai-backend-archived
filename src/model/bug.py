from pydantic import BaseModel

class Bug(BaseModel):
    user_id: str
    date: str
    description: str