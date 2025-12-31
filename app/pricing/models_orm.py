from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean
from datetime import datetime

from app.database import Base


# ---------------------------------------------------------
# EVENTI SPECIALI (per aumenti di prezzo)
# ---------------------------------------------------------

class PricingEvent(Base):
    __tablename__ = "pricing_events"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    multiplier = Column(Float, default=1.10)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)


# ---------------------------------------------------------
# STAGIONALITÀ PERSONALIZZATE
# ---------------------------------------------------------

class SeasonalRule(Base):
    __tablename__ = "seasonal_rules"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    multiplier = Column(Float, default=1.00)
    created_at = Column(DateTime, default=datetime.now)


# ---------------------------------------------------------
# OVERRIDE MANUALI (prezzo fisso)
# ---------------------------------------------------------

class PricingOverride(Base):
    __tablename__ = "pricing_overrides"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    fixed_price = Column(Float, nullable=False)
    reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)


# ---------------------------------------------------------
# PORTALI / PARTNER (moltiplicatori personalizzati)
# ---------------------------------------------------------

class PortalPricing(Base):
    __tablename__ = "portal_pricing"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    portal = Column(String, index=True)
    multiplier = Column(Float, default=1.00)
    created_at = Column(DateTime, default=datetime.now)


# ---------------------------------------------------------
# REGOLE DI PRICING (Dynamic Pricing)
# ---------------------------------------------------------

class PricingRule(Base):
    __tablename__ = "pricing_rules"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    portal = Column(String, nullable=True)

    min_stay = Column(Integer, nullable=True)
    max_stay = Column(Integer, nullable=True)

    percentage = Column(Float, nullable=True)
    fixed_amount = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.now)
