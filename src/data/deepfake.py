from typing import Optional
from bson import ObjectId

from model.deepfake import DeepfakeStatus, DeepfakeUsage, Deepfake
from model.user import User
from model.billing import Plan

from data.billing import get_current_plan

from pymongo import ReturnDocument
from .init import deepfake_col, deepfake_status_col, deepfake_usage_col, plan_col

def get_status(deepfake_id: str) -> Optional[DeepfakeStatus]:
    result = deepfake_status_col.find_one({"_id": deepfake_id})
    if result is not None:
        return DeepfakeStatus(**result)
    else:
        return None

def get_usage(user: User) -> Optional[DeepfakeUsage]:
    result = deepfake_usage_col.find_one({"user_id": user.id})
    if result is not None:
        return DeepfakeUsage(**result)
    else:
        return None
    
def update_usage(user: User) -> Optional[DeepfakeUsage]:
    result = deepfake_usage_col.find_one_and_update(
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

def update_status(deepfake_id: str, output_uri: str) -> Optional[DeepfakeStatus]:
    result = deepfake_status_col.find_one_and_update(
        {"_id": deepfake_id},
        {"$set": {"output_uri": output_uri}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )


    if result is not None:
        return DeepfakeStatus(**result)
    else:
        return None

def has_permissions(user: User) -> bool:
    current_plan = get_current_plan(user)
    usage = get_usage(user)

    if usage and current_plan and usage.generated_num > current_plan.deepfake_num:
        return False
    return True