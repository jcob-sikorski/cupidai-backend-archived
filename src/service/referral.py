from data import referral as data

from model.referral import PayoutRequest

from uuid import uuid4

def update_statistics(user_id: str):
    pass

def generate_link(user_id: str) -> None:
    return generate_link(user_id)

def request_payout(payout_request: PayoutRequest) -> None:
    return data.request_payout(payout_request)

def get_unpaid_earnings(user_id: str) -> float:
    return data.get_unpaid_earnings(user_id)

def get_statistics(user_id: str) -> None:
    return data.get_statistics(user_id)

def get_payout_history(user_id: str) -> None:
    return data.get_payout_history(user_id)