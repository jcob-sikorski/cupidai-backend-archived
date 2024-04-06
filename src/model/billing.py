from pydantic import BaseModel
from typing import List, Optional

class Item(BaseModel):
    data: Optional[dict] = None
    type: Optional[str] = None

class StripeAccount(BaseModel):
    user_id: str
    customer_id: str

class TermsOfService(BaseModel):
    user_id: str
    date_accepted: str