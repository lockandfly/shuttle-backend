from datetime import datetime, timedelta
from app.database import SessionLocal

# IMPORT CORRETTO (i modelli sono in app.bookings.models_orm)
from app.bookings.models_orm import Shuttle, ShuttleAssignment, Booking


# -------------------------
# TIME SLOTS (10 min)
# -------------------------

def compute_time_slots():
    now = datetime.now()
    slots = []

    for i in range(12):  # 2 ore in slot da 10 minuti
        t = now + timedelta(minutes=10 * i)
        slots.append(t.isoformat())

    return {"slots": slots}


# -------------------------
# ASSIGNMENTS (simple)
# -------------------------

def compute_assignments():
    db = SessionLocal()
    now = datetime.now()

    try:
        arrivals = db.query(Booking).filter(
            Booking.checkin >= now,
            Booking.checkin <= now + timedelta(hours=2)
        ).order_by(Booking.checkin.asc()).all()

        shuttles = db.query(Shuttle).filter(
            Shuttle.status.in_(["idle", "returning"])
        ).all()

        assignments = []

        for b in arrivals:
            suitable = [s for s in shuttles if s.capacity >= (b.passenger_count or 1)]
            if not suitable:
                assignments.append({
                    "booking_id": b.id,
                    "status": "no_shuttle_available"
                })
                continue

            chosen = suitable[0]
            assignments.append({
                "booking_id": b.id,
                "shuttle": chosen.name,
                "passengers": b.passenger_count,
                "time": b.checkin
            })

        return {"assignments": assignments}

    finally:
        db.close()


# -------------------------
# FORECAST (next 24h)
# -------------------------

def compute_forecast():
    db = SessionLocal()
    now = datetime.now()

    try:
        forecast = []
        for h in range(24):
            t = now + timedelta(hours=h)
            count = db.query(Booking).filter(
                Booking.checkin <= t,
                Booking.checkout >= t
            ).count()

            forecast.append({"time": t.isoformat(), "cars": count})

        return {"forecast_24h": forecast}

    finally:
        db.close()


# -------------------------
# SCENARIO (increase %)
# -------------------------

def compute_scenario(increase_percent: int):
    base = compute_forecast()["forecast_24h"]

    factor = 1 + (increase_percent / 100)

    scenario = [
        {"time": p["time"], "cars": int(p["cars"] * factor)}
        for p in base
    ]

    return {
        "increase_percent": increase_percent,
        "scenario": scenario
    }


# -------------------------
# FULL OPTIMIZER
# -------------------------

def run_full_optimizer():
    db = SessionLocal()
    now = datetime.now()

    try:
        arrivals = db.query(Booking).filter(
            Booking.checkin >= now,
            Booking.checkin <= now + timedelta(hours=2)
        ).order_by(Booking.checkin.asc()).all()

        shuttles = db.query(Shuttle).filter(
            Shuttle.status.in_(["idle", "returning"])
        ).all()

        assignments = []

        for b in arrivals:
            suitable = [s for s in shuttles if s.capacity >= (b.passenger_count or 1)]
            if not suitable:
                assignments.append({
                    "booking_id": b.id,
                    "status": "no_shuttle_available"
                })
                continue

            chosen = suitable[0]

            assignment = ShuttleAssignment(
                shuttle_id=chosen.id,
                booking_id=b.id,
                timestamp=now
            )
            db.add(assignment)

            chosen.status = "loading"

            assignments.append({
                "booking_id": b.id,
                "shuttle": chosen.name,
                "passengers": b.passenger_count,
                "time": b.checkin
            })

        db.commit()

        return {
            "optimized": True,
            "assignments": assignments,
            "timestamp": now
        }

    finally:
        db.close()


# -------------------------
# DEBUG INFO
# -------------------------

def optimizer_debug_info():
    return {
        "status": "optimizer module loaded",
        "timestamp": datetime.now()
    }
