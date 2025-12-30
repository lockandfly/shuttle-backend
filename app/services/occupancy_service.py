from datetime import datetime, timedelta
from app.database import SessionLocal
from app.bookings.models_orm import Booking


# -------------------------
# BASIC OCCUPANCY
# -------------------------

def get_basic_occupancy():
    now = datetime.now()
    db = SessionLocal()

    try:
        count = db.query(Booking).filter(
            Booking.checkin <= now,
            Booking.checkout >= now
        ).count()

        return {
            "timestamp": now,
            "current_occupancy": count
        }

    finally:
        db.close()


# -------------------------
# ADVANCED OCCUPANCY
# -------------------------

def get_advanced_occupancy():
    now = datetime.now()
    today = now.date()
    db = SessionLocal()

    try:
        # occupazione attuale
        current = db.query(Booking).filter(
            Booking.checkin <= now,
            Booking.checkout >= now
        ).count()

        # forecast 24h
        next_24h = []
        for hour in range(24):
            t = now + timedelta(hours=hour)
            count = db.query(Booking).filter(
                Booking.checkin <= t,
                Booking.checkout >= t
            ).count()
            next_24h.append({"time": t.isoformat(), "cars": count})

        # forecast 7 giorni
        next_7_days = []
        for d in range(7):
            day = today + timedelta(days=d)
            start = datetime(day.year, day.month, day.day)
            end = start + timedelta(days=1)

            count = db.query(Booking).filter(
                Booking.checkin <= end,
                Booking.checkout >= start
            ).count()

            next_7_days.append({
                "date": str(day),
                "cars": count
            })

        return {
            "timestamp": now,
            "current": current,
            "forecast_24h": next_24h,
            "forecast_7_days": next_7_days
        }

    finally:
        db.close()


# -------------------------
# ADVANCED2 OCCUPANCY (FULL VERSION)
# -------------------------

def get_advanced2_occupancy():
    now = datetime.now()
    today = now.date()
    db = SessionLocal()

    try:
        bookings = db.query(Booking).all()

        # 1. OCCUPAZIONE ATTUALE
        current = db.query(Booking).filter(
            Booking.checkin <= now,
            Booking.checkout >= now
        ).count()

        # 2. PREVISIONE 24 ORE
        next_24h = []
        for hour in range(24):
            t = now + timedelta(hours=hour)
            count = db.query(Booking).filter(
                Booking.checkin <= t,
                Booking.checkout >= t
            ).count()
            next_24h.append({"time": t.isoformat(), "cars": count})

        # 3. PREVISIONE 7 GIORNI
        next_7_days = []
        for d in range(7):
            day = today + timedelta(days=d)
            start = datetime(day.year, day.month, day.day)
            end = start + timedelta(days=1)

            count = db.query(Booking).filter(
                Booking.checkin <= end,
                Booking.checkout >= start
            ).count()

            next_7_days.append({
                "date": str(day),
                "cars": count
            })

        # 4. SATURAZIONE PREVISTA
        MAX_CAPACITY = 300
        saturation_points = [
            p for p in next_7_days if p["cars"] >= MAX_CAPACITY
        ]

        # 5. SCENARI
        def simulate_increase(percent):
            factor = 1 + percent / 100
            return [
                {"date": p["date"], "cars": int(p["cars"] * factor)}
                for p in next_7_days
            ]

        scenario_10 = simulate_increase(10)
        scenario_20 = simulate_increase(20)
        scenario_30 = simulate_increase(30)

        # 6. OCCUPAZIONE PER GIORNO DELLA SETTIMANA
        weekday = {i: 0 for i in range(7)}
        for b in bookings:
            if b.checkin and b.checkout:
                for d in range((b.checkout - b.checkin).days + 1):
                    day = b.checkin + timedelta(days=d)
                    weekday[day.weekday()] += 1

        # 7. OCCUPAZIONE PER MESE
        monthly = {}
        for b in bookings:
            if b.checkin and b.checkout:
                month = b.checkin.strftime("%Y-%m")
                monthly.setdefault(month, 0)
                monthly[month] += 1

        # 8. DURATA MEDIA
        durations = [
            (b.checkout - b.checkin).days
            for b in bookings if b.checkin and b.checkout
        ]
        avg_duration = sum(durations) / len(durations) if durations else 0

        # 9. OVERLAP MEDIO
        overlaps = 0
        for b in bookings:
            overlaps += db.query(Booking).filter(
                Booking.id != b.id,
                Booking.checkin <= b.checkout,
                Booking.checkout >= b.checkin
            ).count()

        avg_overlap = overlaps / len(bookings) if bookings else 0

        return {
            "timestamp": now,
            "current": current,
            "forecast_24h": next_24h,
            "forecast_7_days": next_7_days,
            "saturation_points": saturation_points,
            "scenarios": {
                "plus_10_percent": scenario_10,
                "plus_20_percent": scenario_20,
                "plus_30_percent": scenario_30,
            },
            "weekday_occupancy": weekday,
            "monthly_occupancy": monthly,
            "avg_duration_days": avg_duration,
            "avg_overlap": avg_overlap
        }

    finally:
        db.close()
