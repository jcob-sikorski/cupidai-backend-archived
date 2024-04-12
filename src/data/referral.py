from data import referral as data

from model.referral import Referral, Earnings, Statistics, PayoutRequest

from .init import referral_col, payout_request_col, earnings_col, statistics_col, payout_history_col

from uuid import uuid4

from datetime import datetime

def update_statistics(user_id: str, amount_bought: float):
    # Get the current week number, month, and year
    now = datetime.now()
    week_number = now.isocalendar()[1]
    month = now.month
    year = now.year

    # Define the periods
    periods = [
        {"period": "weekly", "period_value": week_number},
        {"period": "monthly", "period_value": month},
        {"period": "yearly", "period_value": year}
    ]

    # For each period
    for period in periods:
        # Try to update the document
        result = statistics_col.update_one(
            {"user_id": user_id, "period": period["period"], "period_value": period["period_value"]},
            {
                "$inc": {
                    "purchases_made": 1,
                    "earned": amount_bought
                }
            }
        )

        # If no document was updated (i.e., it does not exist), create it
        if result.matched_count == 0:
            statistics_col.insert_one(
                {
                    "user_id": user_id,
                    "period": period["period"],
                    "period_value": period["period_value"],
                    "purchases_made": 1,
                    "earned": amount_bought
                }
            )

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