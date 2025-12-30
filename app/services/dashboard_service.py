from datetime import datetime, timedelta
from app.database import SessionLocal
from app.bookings.models_orm import Booking


# -------------------------
# SUMMARY
# -------------------------

def get_dashboard_summary():
    db = SessionLocal()
    now = datetime.now()

    try:
        total_today = db.query(Booking).filter(
            Booking.checkin >= datetime(now.year, now.month, now.day)
        ).count()

        active = db.query(Booking).filter(
            Booking.checkin <= now,
            Booking.checkout >= now
        ).count()

        departures_today = db.query(Booking).filter(
            Booking.checkout >= datetime(now.year, now.month, now.day)
        ).count()

        return {
            "timestamp": now,
            "arrivals_today": total_today,
            "active_now": active,
            "departures_today": departures_today
        }

    finally:
        db.close()


# -------------------------
# ARRIVALS
# -------------------------

def get_arrivals():
    db = SessionLocal()
    now = datetime.now()

    try:
        arrivals = db.query(Booking).filter(
            Booking.checkin >= now,
            Booking.checkin <= now + timedelta(hours=12)
        ).order_by(Booking.checkin.asc()).all()

        return arrivals

    finally:
        db.close()


# -------------------------
# DEPARTURES
# -------------------------

def get_departures():
    db = SessionLocal()
    now = datetime.now()

    try:
        departures = db.query(Booking).filter(
            Booking.checkout >= now,
            Booking.checkout <= now + timedelta(hours=12)
        ).order_by(Booking.checkout.asc()).all()

        return departures

    finally:
        db.close()


# -------------------------
# LIVE STATUS
# -------------------------

def get_live_status():
    db = SessionLocal()
    now = datetime.now()

    try:
        active = db.query(Booking).filter(
            Booking.checkin <= now,
            Booking.checkout >= now
        ).all()

        return {
            "timestamp": now,
            "active_bookings": active
        }

    finally:
        db.close()


# -------------------------
# STATS
# -------------------------

def get_dashboard_stats():
    db = SessionLocal()

    try:
        total = db.query(Booking).count()
        cancelled = db.query(Booking).filter(Booking.status == "cancelled").count()
        completed = db.query(Booking).filter(Booking.status == "completed").count()

        return {
            "total": total,
            "cancelled": cancelled,
            "completed": completed
        }

    finally:
        db.close()


# -------------------------
# PARKING AREAS
# -------------------------

def get_parking_areas_status():
    db = SessionLocal()

    try:
        areas = {}
        bookings = db.query(Booking).all()

        for b in bookings:
            area = b.parking_area or "unknown"
            areas.setdefault(area, 0)
            areas[area] += 1

        return areas

    finally:
        db.close()


# -------------------------
# ALERTS
# -------------------------

def get_alerts():
    db = SessionLocal()
    now = datetime.now()

    try:
        late_arrivals = db.query(Booking).filter(
            Booking.checkin < now - timedelta(hours=1),
            Booking.status != "completed"
        ).all()

        return {
            "late_arrivals": late_arrivals,
            "count": len(late_arrivals)
        }

    finally:
        db.close()


# -------------------------
# HEATMAP
# -------------------------

def get_heatmap():
    db = SessionLocal()

    try:
        heatmap = {}
        bookings = db.query(Booking).all()

        for b in bookings:
            hour = b.checkin.hour if b.checkin else None
            if hour is not None:
                heatmap.setdefault(hour, 0)
                heatmap[hour] += 1

        return heatmap

    finally:
        db.close()


# -------------------------
# FLOW DATA
# -------------------------

def get_flow_data():
    db = SessionLocal()

    try:
        flow = {}
        bookings = db.query(Booking).all()

        for b in bookings:
            day = b.checkin.date() if b.checkin else None
            if day:
                flow.setdefault(str(day), 0)
                flow[str(day)] += 1

        return flow

    finally:
        db.close()


# -------------------------
# TURNOVER
# -------------------------

def get_turnover():
    db = SessionLocal()

    try:
        turnover = {}
        bookings = db.query(Booking).all()

        for b in bookings:
            if b.amount:
                month = b.checkin.strftime("%Y-%m")
                turnover.setdefault(month, 0)
                turnover[month] += b.amount

        return turnover

    finally:
        db.close()
