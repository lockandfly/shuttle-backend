from datetime import datetime, timedelta
from app.database import SessionLocal
from app.bookings.models_orm import Booking


# -------------------------
# TOTAL REVENUE
# -------------------------

def get_total_revenue():
    db = SessionLocal()
    try:
        total = db.query(Booking).filter(Booking.amount != None).all()
        revenue = sum(b.amount for b in total if b.amount)
        return {"total_revenue": revenue}
    finally:
        db.close()


# -------------------------
# DAILY REVENUE
# -------------------------

def get_daily_revenue():
    db = SessionLocal()
    try:
        daily = {}
        bookings = db.query(Booking).filter(Booking.amount != None).all()

        for b in bookings:
            if b.checkin:
                day = b.checkin.date()
                daily.setdefault(str(day), 0)
                daily[str(day)] += b.amount or 0

        return daily
    finally:
        db.close()


# -------------------------
# MONTHLY REVENUE
# -------------------------

def get_monthly_revenue():
    db = SessionLocal()
    try:
        monthly = {}
        bookings = db.query(Booking).filter(Booking.amount != None).all()

        for b in bookings:
            if b.checkin:
                month = b.checkin.strftime("%Y-%m")
                monthly.setdefault(month, 0)
                monthly[month] += b.amount or 0

        return monthly
    finally:
        db.close()


# -------------------------
# PAYMENT METHODS
# -------------------------

def get_payment_methods_stats():
    db = SessionLocal()
    try:
        stats = {}
        bookings = db.query(Booking).all()

        for b in bookings:
            method = b.payment_method or "unknown"
            stats.setdefault(method, 0)
            stats[method] += 1

        return stats
    finally:
        db.close()


# -------------------------
# CANCELLATIONS
# -------------------------

def get_cancellations_stats():
    db = SessionLocal()
    try:
        cancelled = db.query(Booking).filter(Booking.status == "cancelled").count()
        total = db.query(Booking).count()

        return {
            "cancelled": cancelled,
            "total": total,
            "rate": cancelled / total if total > 0 else 0
        }
    finally:
        db.close()


# -------------------------
# FORECAST (simple linear projection)
# -------------------------

def get_revenue_forecast():
    db = SessionLocal()
    now = datetime.now()

    try:
        last_30 = db.query(Booking).filter(
            Booking.checkin >= now - timedelta(days=30),
            Booking.amount != None
        ).all()

        revenue_30 = sum(b.amount for b in last_30 if b.amount)

        daily_avg = revenue_30 / 30 if revenue_30 > 0 else 0

        forecast_30 = daily_avg * 30
        forecast_90 = daily_avg * 90

        return {
            "daily_avg": daily_avg,
            "forecast_30_days": forecast_30,
            "forecast_90_days": forecast_90
        }

    finally:
        db.close()


# -------------------------
# FINANCE KPI
# -------------------------

def get_finance_kpi():
    db = SessionLocal()
    now = datetime.now()

    try:
        bookings = db.query(Booking).all()

        total_revenue = sum(b.amount or 0 for b in bookings)
        avg_ticket = total_revenue / len(bookings) if bookings else 0

        cancelled = len([b for b in bookings if b.status == "cancelled"])
        cancellation_rate = cancelled / len(bookings) if bookings else 0

        payment_methods = {}
        for b in bookings:
            method = b.payment_method or "unknown"
            payment_methods.setdefault(method, 0)
            payment_methods[method] += 1

        return {
            "total_revenue": total_revenue,
            "avg_ticket": avg_ticket,
            "cancellation_rate": cancellation_rate,
            "payment_methods": payment_methods,
            "timestamp": now
        }

    finally:
        db.close()
