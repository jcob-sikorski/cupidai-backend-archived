from typing import List

from model.midjourney import Message
from model.user import User

from pymongo import ReturnDocument
from .init import midjourney_col

def update(message: Message) -> None:
    midjourney_col.find_one_and_update(
        {"message_id": message.message_id},
        {"$set": message.dict()},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

def get_history(user: User) -> List[Message]:
    results = midjourney_col.find({"account_id": user.id})

    messages = [Message(**result) for result in results]

    return messages