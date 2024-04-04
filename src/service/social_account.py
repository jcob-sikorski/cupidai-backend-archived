import data.social_account as data

from service import social_account as service

from model.social_account import SocialAccount
from model.user import User

def create(social_account: SocialAccount, user: User) -> None:
    return data.create(social_account, user)

def update(social_account: SocialAccount, user: User) -> None:
    return data.update(social_account, user)

def get(user: User) -> None:
    return data.get(user)