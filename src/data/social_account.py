from model.social_account import SocialAccount

from pymongo import ReturnDocument
from .init import social_account_col

# TESTING DONE ✅
def create(social_account: SocialAccount, user_id: str) -> bool:
    social_account = social_account.dict()
    social_account['user_id'] = user_id
    result = social_account_col.insert_one(social_account)

    return result.inserted_id is not None

# TESTING DONE ✅
def update(social_account: SocialAccount, user_id: str) -> bool:
    result = social_account_col.find_one_and_update(
        {"user_id": user_id},
        {"$set": social_account.dict()},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    
    return result is not None

# TESTING DONE ✅
def get(user_id: str) -> None:
    results = social_account_col.find({"user_id": user_id})

    social_accounts = [SocialAccount(**result) for result in results]

    return social_accounts