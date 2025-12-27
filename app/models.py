from sqlalchemy import Column, Integer, String, DateTime, Boolean
from .database import Base
from datetime import datetime

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)  # Parkos, MyParking, ecc.
    customer_name = Column(String)
    email = Column(String)
    phone = Column(String)
    car_plate = Column(String)
    arrival = Column(DateTime)
    departure = Column(DateTime)
    notes = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed = Column(Boolean, default=False)
