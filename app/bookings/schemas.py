from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from app.bookings.portal_enum import Portal   # ✅ IMPORT CORRETTO


# ---------------------------------------------------------
# BASE SCHEMA
# ---------------------------------------------------------

class BookingBase(BaseModel):
    customer_name: str
    customer_phone: Optional[str] = None
    license_plate: Optional[str] = None
    arrival_time: datetime
    departure_time: datetime
    portal: Optional[Portal] = Portal.direct
    parking_area: Optional[str] = None
    passenger_count: int = 1
    base_price: float = 0.0


# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------

class BookingCreate(BookingBase):
    pass


# ---------------------------------------------------------
# UPDATE
# ---------------------------------------------------------

class BookingUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    license_plate: Optional[str] = None
    arrival_time: Optional[datetime] = None
    departure_time: Optional[datetime] = None
    portal: Optional[Portal] = None
    parking_area: Optional[str] = None
    passenger_count: Optional[int] = None
    base_price: Optional[float] = None
    final_price: Optional[float] = None


# ---------------------------------------------------------
# READ
# ---------------------------------------------------------

class BookingRead(BaseModel):
    id: int
    customer_name: str
    customer_phone: Optional[str]
    license_plate: Optional[str]
    arrival_time: datetime
    departure_time: datetime
    portal: str
    parking_area: Optional[str]
    passenger_count: int
    base_price: float
    final_price: float
    pricing_breakdown: Optional[dict]
    pricing_reasoning: Optional[str]
    status: str
    raw_data: Optional[dict]

    class Config:
        from_attributes = True
