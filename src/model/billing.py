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
    plan_id: str
    features: List[str]