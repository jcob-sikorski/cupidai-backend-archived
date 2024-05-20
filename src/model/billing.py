from pydantic import BaseModel
from typing import List, Optional

from datetime import datetime

# TODO: probably we can delete this
class Item(BaseModel):
    data: Optional[dict] = None
    type: Optional[str] = None

class PaymentAccount(BaseModel):
    user_id: str
    customer_id: str
    provider: str

class TermsOfService(BaseModel):
    user_id: str | None = None
    date_accepted: datetime | None = None

# TODO: each plan should have each field tied to the specific
#       provider: e.g. radom price_id, radom product_id etc., 
# TODO: for each plan store the chekout link
# class Plan(BaseModel):
#     price_id: str | None = None
#     product_id: str | None = None
#     plan_id: str | None = None
#     name: str | None = None
#     tag: str | None = None
#     description: Optional[str] = None
#     features: List[str] | None = None
#     price: str | None = None

# TODO: probbaly we can delte this
class CreateCheckoutSessionRequest(BaseModel):
    price_id: str | None = None
    referral_id: str | None = None