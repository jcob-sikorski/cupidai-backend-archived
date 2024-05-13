from pydantic import BaseModel
from typing import List, Optional

from datetime import datetime

class Item(BaseModel):
    data: Optional[dict] = None
    type: Optional[str] = None

class StripeAccount(BaseModel):
    user_id: str
    customer_id: str

class TermsOfService(BaseModel):
    user_id: str | None = None
    date_accepted: datetime | None = None

class Plan(BaseModel):
    price_id: str | None = None
    product_id: str | None = None
    name: str | None = None
    tag: str | None = None
    description: Optional[str] = None
    features: List[str] | None = None
    price: str | None = None

class CreateCheckoutSessionRequest(BaseModel):
    price_id: str | None = None
    referral_id: str | None = None