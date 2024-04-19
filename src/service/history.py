import data.history as data

from model.account import Account


def update(domain: str, user_id: str) -> None:
    return data.update(domain, user_id)


def get(user: Account) -> None:
    return data.get(user.user_id)