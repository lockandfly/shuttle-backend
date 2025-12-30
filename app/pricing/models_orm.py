from sqlalchemy import Column, Integer, String, Float, Integer, DateTime
from datetime import datetime

from app.database import Base


class PricingRule(Base):
    __tablename__ = "pricing_rules"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    factor = Column(Float, default=1.0)
    min_days = Column(Integer, nullable=True)
    max_days = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now)


class Discount(Base):
    __tablename__ = "discounts"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    portal = Column(String, index=True)
    percent = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.now)
