from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional

class BookingCreate(BaseModel):
    portal: str
    customer_name: str
    customer_email: Optional[str] = None
    license_plate: Optional[str] = None
    arrival: datetime
    departure: datetime
    price: float
    notes: Optional[str] = None

class BookingRead(BaseModel):
    id: int
    portal: str
    customer_name: str
    customer_email: Optional[str] = None
    license_plate: Optional[str] = None
    arrival: datetime
    departure: datetime
    price: float
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True

class BookingUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    license_plate: Optional[str] = None
    arrival: Optional[datetime] = None
    departure: Optional[datetime] = None
    price: Optional[float] = None
    notes: Optional[str] = None
