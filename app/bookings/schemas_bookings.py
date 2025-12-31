from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class BookingOut(BaseModel):
    id: int
    portal: str
    customer_name: str
    customer_email: Optional[str]
    license_plate: Optional[str]
    arrival: datetime
    departure: datetime
    price: float
    notes: Optional[str]

    class Config:
        orm_mode = True
