from pydantic import BaseModel
from typing import Optional

class SocialAccount(BaseModel):
    profile_uri: str
    name: str
    platform: str
    note: str
    team_id: str
    account_id: str