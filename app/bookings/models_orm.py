from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    portal = Column(String, index=True)
    portal_reservation_id = Column(String, index=True)
    customer_name = Column(String)
    customer_email = Column(String)
    customer_phone = Column(String)
    car_plate = Column(String)
    car_model = Column(String)
    amount = Column(String)
    status = Column(String)
    parking_area = Column(String)
    note = Column(String)
    payment_method = Column(String)
    cancel_reason = Column(String)
    passenger_count = Column(Integer)
    calendar_days = Column(Integer)
    checkin = Column(DateTime)
    checkout = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

# -------------------------
# NAVETTE
# -------------------------

class Shuttle(Base):
    __tablename__ = "shuttles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    capacity = Column(Integer)
    status = Column(String, default="idle")

    assignments = relationship("ShuttleAssignment", back_populates="shuttle")


class ShuttleAssignment(Base):
    __tablename__ = "shuttle_assignments"

    id = Column(Integer, primary_key=True, index=True)
    shuttle_id = Column(Integer, ForeignKey("shuttles.id"))
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    timestamp = Column(DateTime)

    shuttle = relationship("Shuttle", back_populates="assignments")

# -------------------------
# OPERATORI E TURNI
# -------------------------

class Operator(Base):
    __tablename__ = "operators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    role = Column(String)  # es: "navetta", "accettazione", "supervisore"

    shifts = relationship("OperatorShift", back_populates="operator")


class OperatorShift(Base):
    __tablename__ = "operator_shifts"

    id = Column(Integer, primary_key=True, index=True)
    operator_id = Column(Integer, ForeignKey("operators.id"))
    start = Column(DateTime)
    end = Column(DateTime)

    operator = relationship("Operator", back_populates="shifts")
