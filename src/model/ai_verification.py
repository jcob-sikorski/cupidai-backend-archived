from pydantic import BaseModel
from typing import Optional


# TODO: add quality parameter in v2

class Prompt(BaseModel):
    prompt: str | None = None
    account_id: str | None = None
    # generation_speed: str | None = None
    version: str | None = None
    style: str | None = None
    aspect: str | None = None
    stop: str | None = None
    stylize: str | None = None
    seed: str | None = None
    user_id: str | None = None


class SocialAccount(BaseModel):
    account_id: str | None = None
    profile_uri: str | None = None
    passed: bool | None = None
    attempts: str | None = None
    name: str | None = None
    platform: str | None = None
    note: str | None = None
    user_id: str | None = None