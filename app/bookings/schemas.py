from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel


# ---------------------------------------------------------
# BASE SCHEMA (campi comuni)
# ---------------------------------------------------------

class BookingBase(BaseModel):
    portal: Optional[str] = None
    code: Optional[str] = None
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    phone: Optional[str] = None
    customer_phone: Optional[str] = None
    license_plate: Optional[str] = None

    arrival: Optional[datetime] = None
    departure: Optional[datetime] = None

    arrival_time: Optional[datetime] = None
    departure_time: Optional[datetime] = None

    price: Optional[float] = None
    payment_complete: Optional[bool] = None
    external_id: Optional[str] = None
    online_payment: Optional[bool] = None
    payment_option: Optional[str] = None

    cancel_date: Optional[datetime] = None
    cancel_reason: Optional[str] = None

    passengers: Optional[int] = None
    days: Optional[int] = None
    passenger_count: Optional[int] = None

    notes: Optional[str] = None

    parking_area: Optional[str] = None
    base_price: Optional[float] = None
    final_price: Optional[float] = None
    pricing_breakdown: Optional[Any] = None
    pricing_reasoning: Optional[str] = None

    status: Optional[str] = None
    raw_data: Optional[Any] = None


# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------

class BookingCreate(BookingBase):
    portal: str
    arrival: datetime
    departure: datetime


# ---------------------------------------------------------
# READ
# ---------------------------------------------------------

class BookingRead(BookingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------
# UPDATE
# ---------------------------------------------------------

class BookingUpdate(BookingBase):
    pass
