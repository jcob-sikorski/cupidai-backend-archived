from uuid import UUID
from typing import Optional

from model.deepfake import DeepfakeStatus, DeepfakeUsage
from model.user import User

from .init import user_col, deepfake_col, deepfake_status_col, deepfake_usage_col

def get_status(generation_id: UUID) -> Optional[DeepfakeStatus]:
    result = deepfake_status_col.find_one({"_id": generation_id})
    if result is not None:
        return DeepfakeStatus(**result)
    else:
        return None

def get_usage(user: User) -> Optional[DeepfakeUsage]:
    result = deepfake_usage_col.find_one({"_id": user._id})
    if result is not None:
        return DeepfakeUsage(**result)
    else:
        return None

def has_permissions(user: User) -> bool:
    pass

def webhook(deepfake_status: DeepfakeStatus) -> None:
    deepfake_status_col.update_one(
        {"_id": deepfake_status._id},
        {"$set": deepfake_status.dict()},
        upsert=True
    )