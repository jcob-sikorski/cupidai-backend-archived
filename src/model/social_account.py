from pydantic import BaseModel

class SocialAccount(BaseModel):
    profile_uri: str
    name: str
    platform: str
    note: str
    user_id: str