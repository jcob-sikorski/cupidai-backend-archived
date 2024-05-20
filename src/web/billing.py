from fastapi import APIRouter, Depends, Request

from typing import Annotated, List, Tuple, Optional

from model.account import Account
from model.billing import Item, Plan, CreateCheckoutSessionRequest

from service import account as account_service
import service.billing as service

router = APIRouter(prefix="/billing")

@router.post('/webhook')
async def webhook(item: Item, 
                  request: Request) -> None:
    return await service.webhook(item, request)

@router.get("/has-permissions", status_code=200)  # Retrieves the check of access tothe feature
async def has_permissions(feature: str,
                          user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> bool:
    return service.has_permissions(feature,
                                      user)

@router.post('/create-checkout-session', status_code=200)
async def create_checkout_session(create_checkout_session_request: CreateCheckoutSessionRequest,
                                  user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> str:
    return service.create_checkout_session(create_checkout_session_request, 
                                                  user)


@router.get("/current-plan", status_code=200)  # Retrieves current plan of the user
async def get_current_plan(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> Optional[str]:
    return service.get_current_plan(user)


@router.post("/cancel-plan", status_code=201)  # Attempts to cancel current plan of the user
async def cancel_plan(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> bool:
    return service.cancel_plan(user)

# TODO: instead of the available plans route we can use 
#       the plans - which will also return the active plan from these
@router.get("/available-plans", status_code=200)  # Retrieves all available plans
async def get_available_plans(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> Optional[List[Plan]]:
    return service.get_available_plans()

# TODO: do we need product id or something different?
@router.get("/product", status_code=200)  # Retrieves the specific product
async def get_product(product_id: str,
                      user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> Optional[Plan]:
    return service.get_product(product_id)