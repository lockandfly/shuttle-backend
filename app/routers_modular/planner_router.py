from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.planner.schemas import ForecastPlanRead
from app.planner.service import (
    get_forecast_plan,
    generate_forecast,
)

router = APIRouter(
    prefix="",
    tags=["Planner"]
)


@router.get("/forecast/{date}", response_model=ForecastPlanRead | None)
def get_forecast(date: str, db: Session = Depends(get_db)):
    return get_forecast_plan(db, date)


@router.post("/forecast/generate", response_model=list[ForecastPlanRead])
def generate_forecast_plans(days: int = 15, db: Session = Depends(get_db)):
    return generate_forecast(db, days)
