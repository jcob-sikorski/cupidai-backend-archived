import data.social_account as data

from model.account import Account
from model.social_account import SocialAccount

# TESTING DONE ✅
def create(social_account: SocialAccount, user: Account) -> bool:
    return data.create(social_account, user.user_id)

# TESTING DONE ✅
def update(social_account: SocialAccount, user: Account) -> None:
    return data.update(social_account, user.user_id)

# TESTING DONE ✅
def get(user: Account) -> None:
    return data.get(user.user_id)