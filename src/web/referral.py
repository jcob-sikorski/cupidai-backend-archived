from fastapi import APIRouter, Depends

from model.referral import PayoutRequest

from service import referral as service

router = APIRouter(prefix = "/referral")

# TODO: we must track refs in sign up endpoint
#       referrals meaning which plan was bought
#       number of clicks on the link
#       how many purchases were made with this link

# Protected endpoint
@router.post("/link/generate", status_code=201)  # Generates a new link
async def generate_link(user_id: str) -> None:
    return service.generate_link(user_id)

# Protected endpoint
@router.post("/payout/request", status_code=201)  # Requests a payout
async def request_payout(payout_request: PayoutRequest) -> None:
    return service.request_payout(payout_request)

# Protected endpoint
@router.get("/unpaid/", status_code=200)  # Retrieves unpaid earnings
async def get_unpaid_earnings(user_id: str) -> float:
    return service.get_unpaid_earnings(user_id)

# Protected endpoint
@router.get("/statistics", status_code=200)  # Retrieves statistics
async def get_statistics(user_id: str) -> None:
    return service.get_statistics(user_id)

# Protected endpoint
@router.get("/payouts/history", status_code=200)  # Retrieves payout history # TODO: learn in what format there should be the payout
async def get_payout_history(user_id: str) -> None:
    return service.get_payout_history(user_id)