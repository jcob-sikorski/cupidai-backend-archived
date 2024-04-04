import data.bug as data

from model.user import User

def create(description: str, user: User) -> None:
    return data.create(description, user)