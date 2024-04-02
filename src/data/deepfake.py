from pydantic import UUID4
from typing import Optional
from model.deepfake import DeepfakeStatus
from .init import deepfake_status_col  # import the collection from init.py

def get_status(generation_id: UUID4) -> Optional[DeepfakeStatus]:
    result = deepfake_status_col.find_one({"_id": generation_id})  # use the imported collection
    if result is not None:
        return DeepfakeStatus(**result)
    else:
        return None
