from fastapi import APIRouter, Depends

from typing import Annotated

from model.account import Account

from service import account as account_service
from service import bug as service

router = APIRouter(prefix="/bug")

# TESTING DONE ✅
# Protected endpoint
@router.post("/", status_code=201)  # Creates a bug report
async def create(description: str, user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return service.create(description, user)
