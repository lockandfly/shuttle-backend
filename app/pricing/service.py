from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.pricing.models_orm import PricingRule


def calculate_dynamic_price(
    db: Session,
    base_price: float,
    arrival_date: str,
    stay_length: int,
    portal: str,
):
    """
    Calcola il prezzo dinamico applicando le regole presenti nel database.
    """

    # Import interno per evitare import circolare:
    # planner.service → pricing.service → planner.service
    from app.planner.service import get_forecast_plan

    arrival_dt = datetime.fromisoformat(arrival_date)
    adjustments = []
    final_price = base_price

    # 1. Applica regole di pricing dal DB
    rules = db.query(PricingRule).all()
    for rule in rules:
        if rule.portal and rule.portal != portal:
            continue

        if rule.min_stay and stay_length < rule.min_stay:
            continue

        if rule.max_stay and stay_length > rule.max_stay:
            continue

        if rule.percentage:
            delta = final_price * (rule.percentage / 100)
            final_price += delta
            adjustments.append(
                {
                    "rule": rule.name,
                    "type": "percentage",
                    "value": rule.percentage,
                    "delta": delta,
                }
            )

        if rule.fixed_amount:
            final_price += rule.fixed_amount
            adjustments.append(
                {
                    "rule": rule.name,
                    "type": "fixed",
                    "value": rule.fixed_amount,
                    "delta": rule.fixed_amount,
                }
            )

    # 2. Applica forecast (se disponibile)
    forecast = get_forecast_plan(arrival_dt.date())
    if forecast and forecast.occupancy > 0.8:
        delta = final_price * 0.10
        final_price += delta
        adjustments.append(
            {
                "rule": "high_occupancy",
                "type": "percentage",
                "value": 10,
                "delta": delta,
            }
        )

    return {
        "base_price": base_price,
        "final_price": round(final_price, 2),
        "adjustments": adjustments,
        "reasoning": "dynamic pricing applied",
    }
