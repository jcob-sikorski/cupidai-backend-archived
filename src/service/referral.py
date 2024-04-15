from data import referral as data

from model.account import Account
from model.referral import PayoutRequest

def update_statistics(user: Account, amount_bought: float):
    return data.update_statistics(user.user_id, amount_bought)

def generate_link(user: Account) -> None:
    return data.generate_link(user.user_id)

def remove_link(user: Account) -> None:
    return data.remove_link(user.user_id)

def request_payout(payout_request: PayoutRequest) -> None:
    return data.request_payout(payout_request)

def get_unpaid_earnings(user: Account) -> float:
    return data.get_unpaid_earnings(user.user_id)

def get_statistics(user: Account) -> None:
    return data.get_statistics(user.user_id)

def get_payout_history(user: Account) -> None:
    return data.get_payout_history(user.user_id)