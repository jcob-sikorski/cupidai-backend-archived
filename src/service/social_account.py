import data.social_account as data

from model.social_account import SocialAccount

def create(social_account: SocialAccount, user_id: str) -> None:
    return data.create(social_account, user_id)

def update(social_account: SocialAccount, user_id: str) -> None:
    return data.update(social_account, user_id)

def get(user_id: str) -> None:
    return data.get(user_id)