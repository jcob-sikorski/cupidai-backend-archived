from typing import Optional

from model.user import User

from model.deepfake import Deepfake

from pymongo import ReturnDocument
from .init import deepfake_status_col, deepfake_usage_col

def get_status(deepfake_id: str) -> Optional[Deepfake]:
    result = deepfake_status_col.find_one({"_id": deepfake_id})
    if result is not None:
        return Status(**result)
    else:
        return None


def create_status(deepfake_id: str) -> Optional[Status]:
    deepfake_status = Status(output_uri=None, status="in progress")

    result = deepfake_status_col.find_one_and_update(
        {"_id": deepfake_id},
        {"$set": deepfake_status.dict()},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

    if result is not None:
        return Status(**result)
    else:
        return None


def update_status(deepfake_id: str, output_uri: str) -> Optional[Status]:
    result = deepfake_status_col.find_one_and_update(
        {"_id": deepfake_id},
        {"$set": {"output_uri": output_uri}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )


    if result is not None:
        return Status(**result)
    else:
        return None