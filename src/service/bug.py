from fastapi import HTTPException

import data.bug as data

from model.account import Account

# TESTING DONE ✅
def create(description: str, user: Account) -> None:
    if not data.create(description, user.user_id):
        raise HTTPException(status_code=500, detail="Failed to report a bug.")