from typing import Optional
from bson import ObjectId

from model.ai_verification import DeepfakeStatus, DeepfakeUsage, Progress
from model.user import User
from model.billing import Plan

from data.billing import get_current_plan

from pymongo import ReturnDocument
from .init import imagine_progress_col

def get_status(deepfake_id: str) -> Optional[DeepfakeStatus]:
    result = deepfake_status_col.find_one({"_id": deepfake_id})
    if result is not None:
        return DeepfakeStatus(**result)
    else:
        return None

def get_usage_imagine(user: User) -> Optional[DeepfakeUsage]:
    result = deepfake_usage_col.find_one({"user_id": user.id})
    if result is not None:
        return DeepfakeUsage(**result)
    else:
        return None
    
def update_usage_imagine(user: User) -> Optional[DeepfakeUsage]:
    result = imagine_usage_col.find_one_and_update(
        {"user_id": user.id},
        {"$inc": {"generated_num": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

    if result is not None:
        return DeepfakeUsage(**result)
    else:
        return None
    
def create_status(deepfake_id: str) -> Optional[DeepfakeStatus]:
    deepfake_status = DeepfakeStatus(output_uri=None, status="in progress")

    result = deepfake_status_col.find_one_and_update(
        {"_id": deepfake_id},
        {"$set": deepfake_status.dict()},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

    if result is not None:
        return DeepfakeStatus(**result)
    else:
        return None

def update_progress_imagine(progress: Progress) -> None:
    imagine_progress_col.find_one_and_update(
        {"message_id": progress.message_id},
        {"$set": progress.dict()},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

def has_permissions_imagine(user: User) -> bool:
    current_plan = get_current_plan(user)
    usage = get_usage(user)

    if usage and current_plan and usage.generated_num > current_plan.imagine_num:
        return False
    return True