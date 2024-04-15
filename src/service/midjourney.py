from typing import List

import data.midjourney as data
from data.midjourney import Message

from model.account import Account

# TESTING DONE ✅
def webhook(message: Message) -> None:
    data.update(message)

# TESTING DONE ✅
def get_history(user: Account) -> List[Message]:
    return data.get_history(user.user_id)