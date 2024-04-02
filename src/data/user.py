from uuid import uuid4
from typing import Optional
from model.user import User

from pymongo import ReturnDocument
from .init import user_col

def get_user(name: str) -> Optional[User]:
    result = user_col.find_one({"name": name})
    if result is not None:
        return User(**result)
    else:
        return None

def create_user(user: User) -> Optional[User]:
    # Generate a new UUID for the user
    user_id = uuid4()

    # Update the id field of the User object
    user.id = user_id

    result = user_col.find_one_and_update(
        {"_id": user_id},
        {"$set": user.dict()},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

    if result is not None:
        return User(**result)
    else:
        return None
