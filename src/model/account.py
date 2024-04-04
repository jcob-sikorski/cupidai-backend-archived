from pydantic import BaseModel, Field
from typing import Optional

class Account(BaseModel):
    id: str = Field(..., alias='_id')
    theme: str
    two_factor_auth_enabled: bool
    profile_uri: str
    password_hash: str
    email: str