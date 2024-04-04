from pydantic import BaseModel
from typing import List

class TransactionHistory(BaseModel):
    solo: bool
    date: str
    time: str
    payment_id: str
    plan: str
    status: str

class Plan(BaseModel):
    name: str
    price: float
    features: List[str]