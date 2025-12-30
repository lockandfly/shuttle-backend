from fastapi import APIRouter
from app.services.finance_service import (
    get_total_revenue,
    get_daily_revenue,
    get_monthly_revenue,
    get_payment_methods_stats,
    get_cancellations_stats,
    get_revenue_forecast,
    get_finance_kpi
)

router = APIRouter(prefix="/finance", tags=["Finance"])


@router.get("/revenue")
def finance_revenue():
    return get_total_revenue()


@router.get("/revenue/daily")
def finance_revenue_daily():
    return get_daily_revenue()


@router.get("/revenue/monthly")
def finance_revenue_monthly():
    return get_monthly_revenue()


@router.get("/payment_methods")
def finance_payment_methods():
    return get_payment_methods_stats()


@router.get("/cancellations")
def finance_cancellations():
    return get_cancellations_stats()


@router.get("/forecast")
def finance_forecast():
    return get_revenue_forecast()


@router.get("/kpi")
def finance_kpi():
    return get_finance_kpi()
