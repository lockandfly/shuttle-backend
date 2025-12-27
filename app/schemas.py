from pydantic import BaseModel
from datetime import datetime

class BookingBase(BaseModel):
    source: str
    customer_name: str
    email: str
    phone: str
    car_plate: str
    arrival: datetime
    departure: datetime
    notes: str | None = None

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    created_at: datetime
    processed: bool

    class Config:
        orm_mode = True
