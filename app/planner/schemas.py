from pydantic import BaseModel
from datetime import date


class ForecastPlanBase(BaseModel):
    date: date
    occupancy: float


class ForecastPlanRead(ForecastPlanBase):
    id: int

    class Config:
        from_attributes = True
