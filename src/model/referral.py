from pydantic import BaseModel
from typing import List

class PaymentHistory(BaseModel):
    solo: bool
    date: str
    time: str
    payment_id: str
    account_id: str
    amount: float
    status: str

class Statistics(BaseModel):
    solo: bool
    referral_link_clicks: int
    purchases_made: int
    stayed_at_checkout: int
    earned: float
    account_id: str
    month: str
    week: str