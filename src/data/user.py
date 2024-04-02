from pydantic import UUID4
from typing import Optional

from model.user import User

from .init import user_col

def get_user(name: str) -> Optional[User]:
    result = user_col.find_one({"name": name})
    if result is not None:
        return User(**result)
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