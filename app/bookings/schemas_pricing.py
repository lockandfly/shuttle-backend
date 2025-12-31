from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Any


class PricingBase(BaseModel):
    customer_name: str
    customer_phone: Optional[str] = None
    license_plate: str

    arrival_time: datetime
    departure_time: datetime

    portal: Optional[str] = "direct"
    parking_area: Optional[str] = None
    passenger_count: Optional[int] = 1

    base_price: Optional[float] = None
    final_price: Optional[float] = None

    pricing_breakdown: Optional[Any] = None
    pricing_reasoning: Optional[str] = None

    status: Optional[str] = "active"


class PricingCreate(PricingBase):
    pass


class PricingUpdate(BaseModel):
    base_price: Optional[float] = None
    final_price: Optional[float] = None
    pricing_breakdown: Optional[Any] = None
    pricing_reasoning: Optional[str] = None
    status: Optional[str] = None


class PricingOut(PricingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
