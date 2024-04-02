from pydantic import BaseModel, Field

class User(BaseModel):
    id: str = Field(..., alias='_id')
    name: str
    hash: str