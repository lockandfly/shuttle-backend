from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=True)
    license_plate = Column(String, nullable=False)

    arrival_time = Column(DateTime, nullable=False)
    departure_time = Column(DateTime, nullable=False)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
