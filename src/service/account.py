from fastapi import APIRouter

from data import account as data

from model.account import Account
from model.user import User

router = APIRouter(prefix = "/account")

def change_email(email: str, account_id: str, user: User) -> None:
    return data.change_email(email, account_id, user)

def get(account_id: str, user: User) -> None:
    return data.get(account_id, user)

def change_profile_picture(profile_uri: str, account_id: str, user: User) -> None:
    return data.change_profile_picture(profile_uri, account_id, user)

def set_new_password(password: str, account_id: str, user: User) -> None:
    return data.set_new_password(password, account_id, user)

def delete(account_id: str, user: User) -> None:
    return data.delete(account_id, user)

def create(account: Account, user: User) -> None:
    return data.create(account, user)