from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.finance.service import (
    get_daily_revenue,
    get_portal_revenue,
    get_booking_revenue,
)
from app.finance.schemas import (
    DailyRevenueResponse,
    PortalRevenueResponse,
    BookingRevenueResponse,
)

router = APIRouter(
    prefix="",
    tags=["Finance"]
)

# -----------------------------
# DAILY REVENUE
# -----------------------------

@router.get("/daily", response_model=DailyRevenueResponse)
def daily_revenue(db: Session = Depends(get_db)):
    """
    Returns daily revenue aggregated by:
    - date
    - total revenue
    - number of bookings
    """
    return get_daily_revenue(db)


# -----------------------------
# REVENUE BY PORTAL
# -----------------------------

@router.get("/portals", response_model=list[PortalRevenueResponse])
def revenue_by_portal(db: Session = Depends(get_db)):
    """
    Returns revenue grouped by portal:
    - parkos
    - myparking
    - parkingmycar
    - direct
    """
    return get_portal_revenue(db)


# -----------------------------
# REVENUE BY BOOKING
# -----------------------------

@router.get("/bookings", response_model=list[BookingRevenueResponse])
def revenue_by_booking(db: Session = Depends(get_db)):
    """
    Returns revenue for each booking:
    - booking id
    - base price
    - final price
    - portal
    """
    return get_booking_revenue(db)
