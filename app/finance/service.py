from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from app.bookings.models_orm import Booking


# -----------------------------
# DAILY REVENUE
# -----------------------------

def get_daily_revenue(db: Session):
    today = date.today()

    total_revenue = (
        db.query(func.sum(Booking.price))
        .filter(func.date(Booking.arrival) == today)
        .scalar()
    ) or 0.0

    bookings_count = (
        db.query(func.count(Booking.id))
        .filter(func.date(Booking.arrival) == today)
        .scalar()
    ) or 0

    return {
        "date": today,
        "total_revenue": float(total_revenue),
        "bookings_count": bookings_count,
    }


# -----------------------------
# REVENUE BY PORTAL
# -----------------------------

def get_portal_revenue(db: Session):
    rows = (
        db.query(
            Booking.portal,
            func.sum(Booking.price).label("total_revenue"),
            func.count(Booking.id).label("bookings_count"),
        )
        .group_by(Booking.portal)
        .all()
    )

    return [
        {
            "portal": r.portal,
            "total_revenue": float(r.total_revenue or 0),
            "bookings_count": r.bookings_count,
        }
        for r in rows
    ]


# -----------------------------
# REVENUE BY BOOKING
# -----------------------------

def get_booking_revenue(db: Session):
    rows = db.query(
        Booking.id,
        Booking.price,
        Booking.portal,
    ).all()

    return [
        {
            "booking_id": r.id,
            "base_price": float(r.price or 0),
            "final_price": float(r.price or 0),  # placeholder: no dynamic pricing yet
            "portal": r.portal,
        }
        for r in rows
    ]
