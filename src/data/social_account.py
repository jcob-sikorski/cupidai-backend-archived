import data.social_account as data

from service import social_account as service

from model.social_account import SocialAccount
from model.user import User

from pymongo import ReturnDocument
from .init import social_account_col

def create(social_account: SocialAccount, user: User) -> None:
    social_account = social_account.dict()
    social_account['account_id'] = user.id
    social_account_col.insert_one(social_account)

def update(social_account: SocialAccount, user: User) -> None:
    social_account_col.find_one_and_update(
        {"account_id": user.id},
        {"$set": social_account.dict()},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

def get(user: User) -> None:
    results = social_account_col.find({"account_id": user.id})

    social_accounts = [SocialAccount(**result) for result in results]

    return social_accounts