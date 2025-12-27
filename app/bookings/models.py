from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, String, DateTime, Float
import uuid

from app.db.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    portal = Column(String, nullable=False)
    portal_reservation_id = Column(String, nullable=False)

    customer_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    checkin = Column(DateTime, nullable=False)
    checkout = Column(DateTime, nullable=False)

    car_plate = Column(String, nullable=True)

    price = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class BookingCreate(BaseModel):
    portal: str
    portal_reservation_id: str

    customer_name: str
    email: Optional[str] = None
    phone: Optional[str] = None

    checkin: datetime
    checkout: datetime

    car_plate: Optional[str] = None
    price: float


class BookingRead(BaseModel):
    id: str
    portal: str
    portal_reservation_id: str

    customer_name: str
    email: Optional[str]
    phone: Optional[str]

    checkin: datetime
    checkout: datetime

    car_plate: Optional[str]
    price: float

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
