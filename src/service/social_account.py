from typing import List, Optional

from fastapi import HTTPException

import data.social_account as data

from model.account import Account
from model.social_account import SocialAccount


def create(social_account: SocialAccount, 
           user: Account) -> None:
    try:
        data.create(social_account, user.user_id)
    except ValueError:
        raise HTTPException(status_code=500, detail="Failed to create social account")


def update(social_account: SocialAccount) -> None:
    try:
        data.update(social_account)
    except ValueError:
        raise HTTPException(status_code=500, detail="Failed to update social account")


def get(user: Account) -> Optional[List[SocialAccount]]:
    return data.get(user.user_id)