from typing import List

from model.deepfake import Message

from .init import deepfake_col

# TESTING DONE ✅
def create(message: Message) -> bool:
    print("ADDING DEEPFAKE MESSAGE TO THE COLLECTION")
    result = deepfake_col.insert_one(message.dict())
    return result.inserted_id is not None


# TESTING DONE ✅
def update(message_id: str, **kwargs) -> bool:
    print("UPDATING DEEPFAKE MESSAGE IN THE COLLECTION")
    update_fields = {"$set": kwargs}
    result = deepfake_col.update_one({"message_id": message_id}, update_fields)
    return result.modified_count > 0


# TESTING DONE ✅
def get_history(user_id: str) -> List[Message]:
    print("GETTING DEEPFAKE HISTORY")
    results = deepfake_col.find({"user_id": user_id})

    messages = [Message(**result) for result in results]

    return messages