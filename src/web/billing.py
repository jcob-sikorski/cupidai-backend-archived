from fastapi import APIRouter, Depends, Request

from typing import Annotated

from model.account import Account
from model.billing import Item

from service import account as account_service
import service.billing as service

router = APIRouter(prefix="/billing")

# Non-protected endpoint
@router.post('/webhook')
async def webhook(item: Item, request: Request) -> None:
    return await service.webhook(item, request)


# Protected endpoint
@router.get("/download-history", status_code=200)  # Downloads billing history
async def download_history(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return service.download_history(user)


# Protected endpoint
@router.get("/history", status_code=200)  # Retrieves billing history
async def get_history(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return service.get_history(user)
# async def get_history(solo: bool, user_id: str) -> None:
#     return service.get_history(solo, user_id)

# TESTING DONE ✅
# Protected endpoint
@router.post("/terms-of-service", status_code=201)  # Accepts terms of service for billing
async def accept_tos(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return service.accept_tos(user)

# TESTING DONE ✅
# Protected endpoint
@router.get("/current-plan", status_code=200)  # Retrieves current billing plan
async def get_current_plan(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return service.get_current_plan(user)
