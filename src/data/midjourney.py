from typing import List

from model.midjourney import Message

from pymongo import ReturnDocument
from .init import midjourney_col

# TESTING DONE ✅
def update(message: Message) -> None:
    midjourney_col.find_one_and_update(
        {"message_id": message.messageId},
        {"$set": message.dict()},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

# TESTING DONE ✅
def get_history(user_id: str) -> List[Message]:
    results = midjourney_col.find({"ref": user_id})

    messages = [Message(**result) for result in results]
    print(messages)

    return messages