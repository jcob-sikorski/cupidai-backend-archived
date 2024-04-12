from data import referral as data

from model.referral import PayoutRequest

def update_statistics(user_id: str, amount_bought: float):
    return data.update_statistics(user_id, amount_bought)

def generate_link(user_id: str) -> None:
    return generate_link(user_id)

def remove_link(user_id: str) -> None:
    return remove_link(user_id)

def request_payout(payout_request: PayoutRequest) -> None:
    return data.request_payout(payout_request)

def get_unpaid_earnings(user_id: str) -> float:
    return data.get_unpaid_earnings(user_id)

def get_statistics(user_id: str) -> None:
    return data.get_statistics(user_id)

def get_payout_history(user_id: str) -> None:
    return data.get_payout_history(user_id)