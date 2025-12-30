from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, EmailStr


# -------------------------
# BASE
# -------------------------

class BookingBase(BaseModel):
    customer_name: Optional[str] = None
    customer_email: Optional[EmailStr] = None
    checkin: datetime
    checkout: datetime
    passenger_count: Optional[int] = 1
    portal: Optional[str] = None
    parking_area: Optional[str] = None
    raw_data: Optional[Any] = None


# -------------------------
# CREATE
# -------------------------

class BookingCreate(BookingBase):
    pass


# -------------------------
# UPDATE
# -------------------------

class BookingUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_email: Optional[EmailStr] = None
    checkin: Optional[datetime] = None
    checkout: Optional[datetime] = None
    passenger_count: Optional[int] = None
    portal: Optional[str] = None
    parking_area: Optional[str] = None


# -------------------------
# READ
# -------------------------

class BookingRead(BookingBase):
    id: int

    class Config:
        orm_mode = True
