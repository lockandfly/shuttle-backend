from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.planner.models_orm import ForecastPlan


def get_forecast_plan(db: Session, date):
    """
    Restituisce il forecast per una data specifica.
    """

    return (
        db.query(ForecastPlan)
        .filter(ForecastPlan.date == date)
        .first()
    )


def generate_forecast(db: Session, days: int = 15):
    """
    Genera un forecast semplice per i prossimi X giorni.
    """

    today = datetime.now().date()
    plans = []

    for i in range(days):
        date = today + timedelta(days=i)
        occupancy = 0.5  # placeholder
        plan = ForecastPlan(date=date, occupancy=occupancy)
        db.add(plan)
        plans.append(plan)

    db.commit()
    return plans
