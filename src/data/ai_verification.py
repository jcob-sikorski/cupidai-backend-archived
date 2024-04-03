from typing import Optional
from bson import ObjectId

from model.ai_verification import Progress
from model.user import User
from model.billing import Plan

from data.billing import get_current_plan

from pymongo import ReturnDocument
from .init import progress_col
    
def get_usage(user: User) -> Optional[Usage]:
    result = ai_verification_usage_col.find_one({"user_id": user.id})
    if result is not None:
        return Usage(**result)
    else:
        return None


def update_usage(user: User) -> Optional[Usage]:
    result = ai_verification_usage_col.find_one_and_update(
        {"user_id": user.id},
        {"$inc": {"generated_num": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

    if result is not None:
        return Usage(**result)
    else:
        return None


def update_progress(progress: Progress) -> None:
    progress_col.find_one_and_update(
        {"message_id": progress.message_id},
        {"$set": progress.dict()},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )


def update_settings(settings: Settings, user: User) -> :
    ai_verification_settings_col.find_one_and_update(
        {"user_id": user.id},
        {"$set": settings.dict()},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )


def has_permissions(user: User) -> bool:
    current_plan = get_current_plan(user)
    usage = get_usage(user)

    if usage and current_plan and usage.generated_num > current_plan.ai_verification_num:
        return False
    return True