from fastapi import APIRouter
from datetime import datetime

from app.services.pricing_service import (
    calculate_price_service,
    list_pricing_rules,
    create_pricing_rule,
    delete_pricing_rule,
    list_discounts,
    preview_price_service,
)

router = APIRouter(prefix="/pricing", tags=["Pricing"])


@router.get("/calculate")
def pricing_calculate(
    checkin: datetime,
    checkout: datetime,
    portal: str | None = None,
    parking_area: str | None = None,
    passenger_count: int = 1,
):
    return calculate_price_service(
        checkin=checkin,
        checkout=checkout,
        portal=portal,
        parking_area=parking_area,
        passenger_count=passenger_count,
    )


@router.get("/rules")
def pricing_rules():
    return list_pricing_rules()


@router.post("/rules/create")
def pricing_rules_create(
    name: str,
    factor: float,
    min_days: int | None = None,
    max_days: int | None = None,
):
    return create_pricing_rule(name, factor, min_days, max_days)


@router.post("/rules/delete")
def pricing_rules_delete(rule_id: int):
    return delete_pricing_rule(rule_id)


@router.get("/discounts")
def pricing_discounts():
    return list_discounts()


@router.get("/preview")
def pricing_preview(
    checkin: datetime,
    checkout: datetime,
    portal: str | None = None,
    parking_area: str | None = None,
    passenger_count: int = 1,
):
    return preview_price_service(
        checkin=checkin,
        checkout=checkout,
        portal=portal,
        parking_area=parking_area,
        passenger_count=passenger_count,
    )
