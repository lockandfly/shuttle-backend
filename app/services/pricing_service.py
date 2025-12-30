from datetime import datetime
from fastapi import HTTPException

from app.database import SessionLocal
from app.pricing.models_orm import PricingRule, Discount


# -------------------------
# CORE CALCULATION
# -------------------------

def _base_daily_rate(parking_area: str | None) -> float:
    # Placeholder semplice: puoi sostituire con logica reale
    if parking_area == "premium":
        return 12.0
    if parking_area == "standard":
        return 8.0
    return 10.0


def _apply_rules_and_discounts(
    db, base_price: float, days: int, portal: str | None
) -> float:
    price = base_price

    rules = db.query(PricingRule).all()
    for r in rules:
        if (r.min_days is None or days >= r.min_days) and (
            r.max_days is None or days <= r.max_days
        ):
            price *= r.factor

    discounts = db.query(Discount).all()
    for d in discounts:
        if d.portal and portal and d.portal.lower() == portal.lower():
            price *= 1 - (d.percent / 100.0)

    return price


def calculate_price_service(
    checkin: datetime,
    checkout: datetime,
    portal: str | None,
    parking_area: str | None,
    passenger_count: int,
):
    if checkout <= checkin:
        raise HTTPException(status_code=400, detail="Checkout must be after checkin")

    days = max(1, (checkout - checkin).days)
    db = SessionLocal()

    try:
        daily_rate = _base_daily_rate(parking_area)
        base_price = daily_rate * days
        final_price = _apply_rules_and_discounts(db, base_price, days, portal)

        return {
            "checkin": checkin,
            "checkout": checkout,
            "days": days,
            "daily_rate": daily_rate,
            "base_price": base_price,
            "final_price": round(final_price, 2),
            "portal": portal,
            "parking_area": parking_area,
            "passenger_count": passenger_count,
        }

    finally:
        db.close()


# -------------------------
# RULES MANAGEMENT
# -------------------------

def list_pricing_rules():
    db = SessionLocal()
    try:
        return db.query(PricingRule).all()
    finally:
        db.close()


def create_pricing_rule(
    name: str,
    factor: float,
    min_days: int | None,
    max_days: int | None,
):
    db = SessionLocal()
    try:
        rule = PricingRule(
            name=name,
            factor=factor,
            min_days=min_days,
            max_days=max_days,
        )
        db.add(rule)
        db.commit()
        db.refresh(rule)
        return rule
    finally:
        db.close()


def delete_pricing_rule(rule_id: int):
    db = SessionLocal()
    try:
        rule = db.query(PricingRule).filter(PricingRule.id == rule_id).first()
        if not rule:
            raise HTTPException(status_code=404, detail="Pricing rule not found")

        db.delete(rule)
        db.commit()
        return {"deleted": True}
    finally:
        db.close()


# -------------------------
# DISCOUNTS
# -------------------------

def list_discounts():
    db = SessionLocal()
    try:
        return db.query(Discount).all()
    finally:
        db.close()


# -------------------------
# PREVIEW
# -------------------------

def preview_price_service(
    checkin: datetime,
    checkout: datetime,
    portal: str | None,
    parking_area: str | None,
    passenger_count: int,
):
    result = calculate_price_service(
        checkin=checkin,
        checkout=checkout,
        portal=portal,
        parking_area=parking_area,
        passenger_count=passenger_count,
    )
    result["preview"] = True
    return result
