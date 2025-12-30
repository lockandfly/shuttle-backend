from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database import Base


class Operator(Base):
    __tablename__ = "operators"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)  # es: "valet", "driver", "manager"
    phone = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
