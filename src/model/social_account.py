from pydantic import BaseModel

class SocialAccount(BaseModel):
    account_id: str | None = None
    profile_uri: str | None = None
    name: str | None = None
    platform: str | None = None
    note: str | None = None
    user_id: str | None = None