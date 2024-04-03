from typing import Optional
from bson import ObjectId

from model.ai_verification import Progress
from model.user import User
from model.billing import Plan

from data.billing import get_current_plan

from pymongo import ReturnDocument
from .init import progress_col
    
def get_usage(user: User) -> Optional[Usage]:
    result = usage_col.find_one({"user_id": user.id})
    if result is not None:
        return Usage(**result)
    else:
        return None


def update_usage(user: User) -> Optional[Usage]:
    result = usage_col.find_one_and_update(
        {"user_id": user.id},
        {"$inc": {"generated_num": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

    if result is not None:
        return Usage(**result)
    else:
        return None