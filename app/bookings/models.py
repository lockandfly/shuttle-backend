from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BookingRead(BaseModel):
    id: str
    portal: str
    portal_reservation_id: str
    customer_name: str
    checkin: datetime
    checkout: datetime
    updated_at: datetime

    # Campi opzionali per futuri portali/API/email
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    surname: Optional[str] = None
    name: Optional[str] = None
    vehicle: Optional[str] = None
    type: Optional[str] = None
    created_at: Optional[datetime] = None
