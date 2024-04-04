from model.account import Account
from model.user import User

from pymongo import ReturnDocument
from .init import account_col

def change_email(email: str, account_id: str, user: User) -> None:
    account_col.find_one_and_update(
        {"account_id": account_id},
        {"$set": {"email": email}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

def get(account_id: str, user: User) -> None:
    result = account_col.find_one({"account_id": account_id})
    
    if result is not None:
        return Account(**result)
    else:
        return None

def change_profile_picture(profile_uri: str, account_id: str, user: User) -> None:
    account_col.find_one_and_update(
        {"account_id": account_id},
        {"$set": {"profile_uri": profile_uri}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

def set_new_password(password: str, account_id: str, user: User) -> None:
    account_col.find_one_and_update(
        {"account_id": account_id},
        {"$set": {"password": password}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

def delete(account_id: str, user: User) -> None:
    account_col.delete_one({"account_id": account_id})

def create(account: Account, user: User) -> None:
    account_col.insert_one(account.dict())