from typing import List

from model.deepfake import Deepfake

from model.user import User

from .init import deepfake_col

def get_history(user: User) -> List[Deepfake]:
    results = deepfake_col.find({"account_id": user.id})

    deepfakes = [Deepfake(**result) for result in results]

    return deepfakes