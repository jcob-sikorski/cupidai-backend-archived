import data.history as data

from model.account import Account

# TESTING DONE ✅
def update(domain: str, user: Account) -> None:
    return data.update(domain, user.user_id)

# TESTING DONE ✅
def get(user: Account) -> None:
    return data.get(user.user_id)