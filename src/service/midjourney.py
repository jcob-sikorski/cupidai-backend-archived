from typing import List

import data.midjourney as data

from data.midjourney import Message

# TESTING DONE ✅
def webhook(message: Message) -> None:
    data.update(message)

def get_history(user_id: str) -> List[Message]:
    return data.get_history(user_id)