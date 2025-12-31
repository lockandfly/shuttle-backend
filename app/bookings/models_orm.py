from sqlalchemy import Column, Integer, String, DateTime, Float, JSON
from datetime import datetime

from app.database import Base


class Booking(Base):
    __tablename__ = "bookings_pricing"   # ← TABELLA DEDICATA AL DYNAMIC PRICING
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=True)
    license_plate = Column(String, nullable=False)

    arrival_time = Column(DateTime, nullable=False)
    departure_time = Column(DateTime, nullable=False)

    # Dynamic Pricing fields
    portal = Column(String, nullable=True, default="direct")
    parking_area = Column(String, nullable=True)
    passenger_count = Column(Integer, default=1)

    base_price = Column(Float, nullable=True)
    final_price = Column(Float, nullable=True)

    pricing_breakdown = Column(JSON, nullable=True)
    pricing_reasoning = Column(String, nullable=True)

    # Status
    status = Column(String, default="active")  # active | completed | cancelled

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
