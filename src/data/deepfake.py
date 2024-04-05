from typing import List

from model.deepfake import Deepfake

from .init import deepfake_col

def get_history(user_id: str) -> List[Deepfake]:
    results = deepfake_col.find({"user_id": user_id})

    deepfakes = [Deepfake(**result) for result in results]

    return deepfakes