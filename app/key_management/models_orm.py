from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class KeySlot(Base):
    __tablename__ = "keyslots"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, nullable=False)  # es: "A12", "B03"
    description = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationship
    movements = relationship("KeyMovement", back_populates="keyslot", cascade="all, delete")


class KeyMovement(Base):
    __tablename__ = "key_movements"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    keyslot_id = Column(Integer, ForeignKey("keyslots.id"), nullable=False)
    operator_name = Column(String, nullable=False)
    action = Column(String, nullable=False)  # "pickup" | "return"
    timestamp = Column(DateTime, default=datetime.now)

    keyslot = relationship("KeySlot", back_populates="movements")
