from datetime import datetime
from pydantic import BaseModel


class BookingBase(BaseModel):
    portal: str
    code: str | None = None
    customer_name: str | None = None
    customer_email: str | None = None
    phone: str | None = None
    license_plate: str | None = None

    arrival: datetime
    departure: datetime

    price: float | None = None

    payment_complete: bool | None = None
    external_id: str | None = None
    online_payment: bool | None = None
    payment_option: str | None = None

    cancel_date: datetime | None = None
    cancel_reason: str | None = None

    passengers: int | None = None
    days: int | None = None

    notes: str | None = None


class BookingResponse(BookingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
