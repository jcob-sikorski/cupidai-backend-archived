import data.bug as data

from model.account import Account

# TESTING DONE ✅
def create(description: str, user: Account) -> None:
    return data.create(description, user.user_id)