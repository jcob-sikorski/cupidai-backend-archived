from pydantic import BaseModel

class Account(BaseModel):
    user_id: str
    email: str