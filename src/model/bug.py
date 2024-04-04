from pydantic import BaseModel

class Bug(BaseModel):
    account_id: str
    date: str
    description: str