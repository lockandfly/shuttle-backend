from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------

class BookingCreate(BaseModel):
    customer_name: str
    customer_phone: Optional[str] = None
    license_plate: str
    arrival_time: datetime
    departure_time: datetime


# ---------------------------------------------------------
# UPDATE
# ---------------------------------------------------------

class BookingUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    license_plate: Optional[str] = None
    arrival_time: Optional[datetime] = None
    departure_time: Optional[datetime] = None


# ---------------------------------------------------------
# READ
# ---------------------------------------------------------

class BookingRead(BaseModel):
    id: int
    customer_name: str
    customer_phone: Optional[str]
    license_plate: str
    arrival_time: datetime
    departure_time: datetime
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
