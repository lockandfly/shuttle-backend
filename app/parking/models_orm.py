from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum,
    Float,
)
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database import Base


# ---------------------------------------------------------
# ENUM
# ---------------------------------------------------------

class SpotStatus(str, enum.Enum):
    FREE = "free"
    OCCUPIED = "occupied"
    RESERVED = "reserved"


# ---------------------------------------------------------
# PARKING AREA ORM
# ---------------------------------------------------------

class ParkingArea(Base):
    __tablename__ = "parking_areas"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    total_spots = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationship
    spots = relationship("ParkingSpot", back_populates="area", cascade="all, delete")


# ---------------------------------------------------------
# PARKING SPOT ORM
# ---------------------------------------------------------

class ParkingSpot(Base):
    __tablename__ = "parking_spots"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    area_id = Column(Integer, ForeignKey("parking_areas.id"), nullable=False)

    spot_number = Column(String, nullable=False)
    status = Column(Enum(SpotStatus), default=SpotStatus.FREE)

    x = Column(Float, nullable=True)
    y = Column(Float, nullable=True)

    keyslot_id = Column(Integer, nullable=True)
    booking_id = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationship
    area = relationship("ParkingArea", back_populates="spots")
