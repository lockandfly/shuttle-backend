from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.bookings.models_orm import Booking
from app.bookings.schemas import BookingCreate, BookingUpdate


# ---------------------------------------------------------
# CREATE BOOKING
# ---------------------------------------------------------

def create_booking(db: Session, data: BookingCreate):
    booking = Booking(**data.model_dump())
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


# ---------------------------------------------------------
# LIST ALL BOOKINGS
# ---------------------------------------------------------

def list_bookings(db: Session):
    return db.query(Booking).all()


# ---------------------------------------------------------
# GET SINGLE BOOKING
# ---------------------------------------------------------

def get_booking(db: Session, booking_id: int):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


# ---------------------------------------------------------
# UPDATE BOOKING
# ---------------------------------------------------------

def update_booking(db: Session, booking_id: int, data: BookingUpdate):
    booking = get_booking(db, booking_id)

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(booking, field, value)

    db.commit()
    db.refresh(booking)
    return booking


# ---------------------------------------------------------
# DELETE BOOKING
# ---------------------------------------------------------

def delete_booking(db: Session, booking_id: int):
    booking = get_booking(db, booking_id)
    db.delete(booking)
    db.commit()
    return {"deleted": True}
