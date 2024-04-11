from pydantic import BaseModel

class Account(BaseModel):
    user_id: str
    email: str

class Invite(BaseModel):
    invite_id: str
    guest_id: str
    host_id: str
    signup_required: bool