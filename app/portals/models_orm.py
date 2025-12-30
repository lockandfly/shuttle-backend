from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime

from app.database import Base


class PortalConfig(Base):
    __tablename__ = "portal_configs"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    portal_name = Column(String, unique=True, index=True)
    settings = Column(JSON, default={})
    updated_at = Column(DateTime, default=datetime.now)


class PortalMapping(Base):
    __tablename__ = "portal_mappings"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    portal_name = Column(String, index=True)
    field = Column(String)
    mapped_to = Column(String)
