from typing import List

from model.deepfake import Deepfake

from .init import deepfake_col

# TESTING DONE ✅
def create(deepfake: Deepfake) -> bool:
    print("ADDING DEEPFAKE TO THE COLLECTION")
    result = deepfake_col.insert_one(deepfake.dict())
    return result.inserted_id is not None


# TESTING DONE ✅
def update(deepfake_id: str, **kwargs) -> bool:
    print("UPDATING DEEPFAKE IN THE COLLECTION")
    update_fields = {"$set": kwargs}
    result = deepfake_col.update_one({"deepfake_id": deepfake_id}, update_fields)
    return result.modified_count > 0


# TESTING DONE ✅
def get_history(user_id: str) -> List[Deepfake]:
    print("GETTING DEEPFAKE HISTORY")
    results = deepfake_col.find({"user_id": user_id})

    deepfakes = [Deepfake(**result) for result in results]

    return deepfakes