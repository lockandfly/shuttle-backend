from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.sql import func
from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    # Identificativo portale (parkos, myparking, direct, parkingmycar)
    portal = Column(String, index=True, nullable=False)

    # Campi normalizzati Parkos
    code = Column(String, nullable=True)
    customer_name = Column(String, nullable=True)
    customer_email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    license_plate = Column(String, nullable=True)

    arrival = Column(DateTime, nullable=False)
    departure = Column(DateTime, nullable=False)

    price = Column(Float, nullable=True)

    payment_complete = Column(Boolean, nullable=True)
    external_id = Column(String, nullable=True)
    online_payment = Column(Boolean, nullable=True)
    payment_option = Column(String, nullable=True)

    cancel_date = Column(DateTime, nullable=True)
    cancel_reason = Column(String, nullable=True)

    passengers = Column(Integer, nullable=True)
    days = Column(Integer, nullable=True)

    # Campo interno
    notes = Column(String, nullable=True)

    # Timestamp automatici
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
