import data.history as data

from model.user import User

def update(domain: str, user: User) -> None:
    return data.update(domain, user)

def get(user: User) -> None:
    return data.get(user)