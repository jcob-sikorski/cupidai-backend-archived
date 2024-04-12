from data import referral as data

from model.referral import Referral, Earnings, Statistics, PayoutRequest

from .init import referral_col, payout_request_col, earnings_col, statistics_col, payout_history_col

from uuid import uuid4

def update_statistics(user_id: str):
    pass

def generate_link(user_id: str) -> None:
    referral_id = str(uuid4())

    referral = Referral(
        referral_id=referral_id,
        user_id=user_id
    )

    referral_col.insert_one(referral.dict())

    return referral_id


def request_payout(payout_request: PayoutRequest) -> None:
    payout_request_col.insert_one(payout_request.dict())

def get_unpaid_earnings(user_id: str) -> float:
    earnings = earnings_col.find_one({"user_id": user_id})

    if earnings and earnings['amount'] > 0:
        return earnings['amount']

    return 0.00

def get_statistics(user_id: str) -> None:
    statistics = statistics_col.find_one({"user_id": user_id})

    if statistics:
        return Statistics(**statistics)

    return None

def get_payout_history(user_id: str) -> None:
    payout_history = payout_history_col.find_one({"user_id": user_id})

    if payout_history:
        return Statistics(**payout_history)

    return None