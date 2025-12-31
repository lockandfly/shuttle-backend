from sqlalchemy import Column, Integer, Date, Float
from app.database import Base


class ForecastPlan(Base):
    __tablename__ = "forecast_plan"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, index=True)
    occupancy = Column(Float, nullable=False)
