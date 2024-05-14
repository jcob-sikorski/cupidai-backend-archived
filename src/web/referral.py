from fastapi import APIRouter, Depends

from typing import Annotated

from model.account import Account
from model.referral import PayoutRequest

from service import account as account_service
from service import referral as service

router = APIRouter(prefix = "/referral")


@router.post("/link/generate", status_code=201)  # Generates a new link
async def generate_link(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> str:
    return service.generate_link(user)


@router.post("/link-clicked", status_code=201)
async def link_clicked(referral_id: str) -> None:
    return await service.link_clicked(referral_id)


@router.post("/payout/request", status_code=201)  # Requests a payout
async def request_payout(payout_request: PayoutRequest, 
                         _: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return service.request_payout(payout_request)


@router.get("/unpaid", status_code=200)  # Retrieves unpaid earnings
async def get_unpaid_earnings(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> float:
    return service.get_unpaid_earnings(user)


@router.get("/statistics", status_code=200)  # Retrieves statistics
async def get_statistics(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return service.get_statistics(user)


@router.get("/payouts/history", status_code=200)  # Retrieves payout history
async def get_payout_history(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return service.get_payout_history(user)