from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


# ---------------------------------------------------------
# SHUTTLE (CRUD)
# ---------------------------------------------------------

class Shuttle(Base):
    __tablename__ = "shuttles"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    plate = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)

    logs = relationship("ShuttleLog", back_populates="shuttle", cascade="all, delete")
    movements = relationship("ShuttleMovement", back_populates="shuttle", cascade="all, delete")


# ---------------------------------------------------------
# SHUTTLE LOGS
# ---------------------------------------------------------

class ShuttleLog(Base):
    __tablename__ = "shuttle_logs"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    shuttle_id = Column(Integer, ForeignKey("shuttles.id"), nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)

    shuttle = relationship("Shuttle", back_populates="logs")


# ---------------------------------------------------------
# SHUTTLE MOVEMENTS (Tracking)
# ---------------------------------------------------------

class ShuttleMovement(Base):
    __tablename__ = "shuttle_movements"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    shuttle_id = Column(Integer, ForeignKey("shuttles.id"), nullable=False)
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=False)

    action = Column(String, nullable=False)  # "depart" | "arrive"
    notes = Column(String, nullable=True)

    timestamp = Column(DateTime, default=datetime.now)

    shuttle = relationship("Shuttle", back_populates="movements")
    operator = relationship("Operator")
