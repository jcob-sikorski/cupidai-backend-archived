from fastapi import APIRouter, Depends, Request

from typing import Annotated, List, Optional

from model.account import Account
from model.billing import Item, Plan

from service import account as account_service
import service.billing as service

router = APIRouter(prefix="/billing")

@router.post('/webhook')
async def webhook(item: Item, 
                  request: Request) -> None:
    return await service.webhook(item, request)

@router.post('/create-checkout-session')
async def create_checkout_session(referral_id: str, 
                                  user: Annotated[Account, Depends(account_service.get_current_active_user)]
                                  ) -> None:
    session_url = await service.create_checkout_session(referral_id, user)

    return {"session_url": session_url}

# TODO: user need to download history in chunks
@router.get("/download-history", status_code=200)  # Downloads billing history
async def download_history(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return service.download_history(user)


@router.get("/history", status_code=200)  # Retrieves billing history
async def get_history(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> dict:
    return service.get_history(user)



@router.post("/terms-of-service", status_code=201)  # Accepts terms of service for billing
async def accept_tos(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return service.accept_tos(user)



@router.get("/current-plan", status_code=200)  # Retrieves current billing plan
async def get_current_plan(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> Optional[Plan]:
    return service.get_current_plan(user)

@router.get("/available-plans", status_code=200)  # Retrieves all available plans
async def get_available_plans(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> Optional[List[Plan]]:
    product_list = service.get_available_plans()

    return product_list