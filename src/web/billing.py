from fastapi import APIRouter, Depends, Request

from typing import Annotated, Optional, Dict, Any

from model.account import Account
from model.billing import Plan, CheckoutSessionRequest

from service import account as account_service
import service.billing as service

router = APIRouter(prefix="/billing")


@router.get("/has-permissions", status_code=200)  # Retrieves the check of access tothe feature
async def has_permissions(feature: str,
                          user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> bool:
    return service.has_permissions(feature,
                                      user)


@router.post('/create-checkout-session', status_code=200)
async def create_checkout_session(req: CheckoutSessionRequest,
                                  user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return service.create_checkout_session(req,
                                           user)


# TODO: this will accept the event type "managedRecurringPayment" some event 
#       data and radomData which contains the checkoutSessionId
@router.post('/webhook')
async def webhook(request: Request) -> None:
    return await service.webhook(request)


@router.post("/cancel-plan", status_code=201)  # Attempts to cancel current plan of the user
async def cancel_plan(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> bool:
    return service.cancel_plan(user)


@router.get("/available-plans", status_code=200)  # Retrieves all available plans
async def get_available_plans(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> Optional[Dict[str, Any]]:
    return service.get_available_plans(user)


@router.get("/product", status_code=200)  # Retrieves the specific product
async def get_product(radom_product_id: str,
                      user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> Optional[Plan]:
    return service.get_product(radom_product_id)