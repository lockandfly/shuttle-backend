from pydantic import BaseModel
from typing import List, Optional


# -----------------------------
# REQUEST
# -----------------------------

class PricingRequest(BaseModel):
    base_price: float
    arrival_date: str
    stay_length: int
    portal: str


# -----------------------------
# RESPONSE
# -----------------------------

class PricingAdjustment(BaseModel):
    rule: str
    type: str
    value: float
    delta: float


class PricingResponse(BaseModel):
    base_price: float
    final_price: float
    adjustments: List[PricingAdjustment]
    reasoning: str
