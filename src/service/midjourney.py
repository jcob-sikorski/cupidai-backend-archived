from typing import List

import data.midjourney as data

from data.midjourney import Message

from model.user import User

def webhook(message: Message) -> None:
    data.update(message)

def get_history(user: User) -> List[Message]:
    return data.get_history(user)