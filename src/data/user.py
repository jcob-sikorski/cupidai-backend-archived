from pydantic import UUID4
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
    result = user_col.find_one_and_update(
        {"_id": user._id},
        {"$set": user.dict()},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    if result is not None:
        return User(**result)
    else:
        return None
