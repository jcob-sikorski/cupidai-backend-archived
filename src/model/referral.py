from pydantic import BaseModel
from typing import List

class PaymentHistory(BaseModel):
    solo: bool
    date: str
    time: str
    payment_id: str
    user_id: str
    amount: float
    status: str

class Statistics(BaseModel):
    solo: bool
    referral_link_clicks: int
    purchases_made: int
    stayed_at_checkout: int
    earned: float
    user_id: str
    month: str  # TODO: probably we can merge this into a single date so we use mognodb filters for getting stats by week, month, etc.
    week: str   # TODO: probably we can merge this into a single date so we use mognodb filters for getting stats by week, month, etc.