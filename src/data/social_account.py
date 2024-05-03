from typing import List, Optional

from model.social_account import SocialAccount

from pymongo import ReturnDocument
from .init import social_account_col


def create(social_account: SocialAccount, 
           user_id: str) -> None:
    social_account = social_account.dict()
    social_account['user_id'] = user_id
    result = social_account_col.insert_one(social_account)

    if not result:
        raise ValueError("Failed to create social account.")


def update(social_account: SocialAccount) -> bool:
    result = social_account_col.find_one_and_update(
        {"account_id": social_account.account_id},
        {"$set": social_account.dict()},
        upsert=False,
        return_document=ReturnDocument.AFTER
    )

    if not result:
        raise ValueError("Failed to update social account.")


def get(user_id: str) -> Optional[List[SocialAccount]]:
    results = social_account_col.find({"user_id": user_id})

    social_accounts = [SocialAccount(**result) for result in results]

    return social_accounts