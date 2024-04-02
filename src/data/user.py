from bson import ObjectId
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

def create_user(name: str, hash: str) -> Optional[User]:
    user_id = str(ObjectId())

    user = User(name=name, hash=hash, id=user_id)

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