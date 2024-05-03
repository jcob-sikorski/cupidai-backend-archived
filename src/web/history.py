from fastapi import APIRouter, Depends

# TODO: this should be renamed to usage_history

from typing import Annotated

import data.history as data

from model.account import Account
from model.history import History

from service import account as account_service

router = APIRouter(prefix="/history")



@router.get("/", status_code=200)  # Retrieves account details
async def get(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> History:
    return data.get(user.user_id)
