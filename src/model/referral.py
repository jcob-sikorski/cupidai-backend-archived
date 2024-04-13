from pydantic import BaseModel
from typing import List

class PayoutRequest(BaseModel):
    user_id: str
    withdrawal_method: str
    paypal_email: List[str]
    amount: List[float]
    scheduled_time: str
    # team_notes: str
    date: str

class PayoutHistory(BaseModel):
    date: str
    payment_id: str
    user_id: str
    amount: float
    status: str

class Earnings(BaseModel):
    user_id: str
    amount: float

class Statistics(BaseModel):
    period: str  # This can be 'weekly', 'monthly', or 'yearly'
    period_value: int  # This can be week number, month number, or year
    # referral_link_clicks: int TODO: update this when calling the singup/ref endpoint
    purchases_made: int
    earned: float
    user_id: str

# this is for a single generated link
# its idea is to securely map a link to the user_id
class Referral(BaseModel):
    referral_id: str
    user_id: str