from datetime import datetime
from app.database import SessionLocal

# I MODELLI SONO IN bookings
from app.bookings.models_orm import Shuttle, ShuttleAssignment, ShuttleQueue, Booking


def list_shuttles():
    db = SessionLocal()
    try:
        return db.query(Shuttle).all()
    finally:
        db.close()


def create_shuttle(name: str, capacity: int):
    db = SessionLocal()
    try:
        shuttle = Shuttle(name=name, capacity=capacity, status="idle")
        db.add(shuttle)
        db.commit()
        db.refresh(shuttle)
        return shuttle
    finally:
        db.close()


def update_shuttle_status(shuttle_id: int, status: str):
    db = SessionLocal()
    try:
        shuttle = db.query(Shuttle).filter(Shuttle.id == shuttle_id).first()
        if not shuttle:
            return {"error": "Shuttle not found"}

        shuttle.status = status
        db.commit()
        db.refresh(shuttle)
        return shuttle
    finally:
        db.close()


def assign_shuttle(booking_id: int, shuttle_id: int):
    db = SessionLocal()
    now = datetime.now()

    try:
        assignment = ShuttleAssignment(
            shuttle_id=shuttle_id,
            booking_id=booking_id,
            timestamp=now
        )
        db.add(assignment)
        db.commit()
        db.refresh(assignment)
        return assignment
    finally:
        db.close()


def get_shuttle_queue():
    db = SessionLocal()
    try:
        return db.query(ShuttleQueue).order_by(ShuttleQueue.position.asc()).all()
    finally:
        db.close()


def add_to_queue(shuttle_id: int):
    db = SessionLocal()
    try:
        last = db.query(ShuttleQueue).order_by(ShuttleQueue.position.desc()).first()
        next_pos = (last.position + 1) if last else 1

        entry = ShuttleQueue(shuttle_id=shuttle_id, position=next_pos)
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
    finally:
        db.close()
