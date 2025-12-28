from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BookingRead(BaseModel):
    # campi minimi comuni
    id: str
    portal: str
    portal_reservation_id: str
    customer_name: str
    checkin: datetime
    checkout: datetime
    updated_at: datetime

    # campi opzionali (MyParking, Parkos, ParkingMyCar, API future)
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    car_plate: Optional[str] = None
    car_model: Optional[str] = None
    amount: Optional[str] = None
    status: Optional[str] = None
    parking_area: Optional[str] = None
    created_at: Optional[datetime] = None
    note: Optional[str] = None

    # estensioni Parkos
    payment_method: Optional[str] = None
    cancel_reason: Optional[str] = None
    passenger_count: Optional[int] = None
    calendar_days: Optional[int] = None
