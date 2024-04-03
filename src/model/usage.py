from pydantic import BaseModel

class Usage(BaseModel):
    user_id: str
    generated_num: int