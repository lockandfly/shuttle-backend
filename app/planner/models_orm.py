from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Plan(Base):
    __tablename__ = "plans"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now)

    items = relationship("PlanItem", back_populates="plan")


class PlanItem(Base):
    __tablename__ = "plan_items"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"))
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.now)

    plan = relationship("Plan", back_populates="items")
