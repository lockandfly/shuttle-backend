from pydantic import BaseModel
from datetime import date
from typing import Optional


# -----------------------------
# DAILY REVENUE
# -----------------------------

class DailyRevenueResponse(BaseModel):
    date: date
    total_revenue: float
    bookings_count: int


# -----------------------------
# REVENUE BY PORTAL
# -----------------------------

class PortalRevenueResponse(BaseModel):
    portal: str
    total_revenue: float
    bookings_count: int


# -----------------------------
# REVENUE BY BOOKING
# -----------------------------

class BookingRevenueResponse(BaseModel):
    booking_id: int
    base_price: float
    final_price: float
    portal: str
