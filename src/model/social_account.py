from pydantic import BaseModel

# TODO: associate account with each prompt document 
#       from ai_verification by id
#       so user can fetch the prompt attached to the account by the account_id

# TODO: there should be the endpoint which based on the user_id gets all accounts and the prompt details and returns them in two lists: social account and prompt

class SocialAccount(BaseModel):
    account_id: str | None = None
    profile_uri: str | None = None
    passed: bool | None = None
    attempts: bool | None = None
    name: str | None = None
    platform: str | None = None
    note: str | None = None
    user_id: str | None = None