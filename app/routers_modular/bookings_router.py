from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.bookings.models import Booking
from app.bookings.schemas_bookings import BookingOut

router = APIRouter(prefix="/bookings", tags=["Bookings Import"])


# ---------------------------------------------------------
# GET ALL BOOKINGS
# ---------------------------------------------------------
@router.get("/", response_model=list[BookingOut])
def get_all_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()


# ---------------------------------------------------------
# GET BOOKING BY ID
# ---------------------------------------------------------
@router.get("/{booking_id}", response_model=BookingOut)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")
    return booking


# ---------------------------------------------------------
# DELETE BOOKING
# ---------------------------------------------------------
@router.delete("/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")

    db.delete(booking)
    db.commit()

    return {"status": "deleted", "id": booking_id}


# ---------------------------------------------------------
# SEARCH BOOKINGS (targa, nome, portale)
# ---------------------------------------------------------
@router.get("/search/", response_model=list[BookingOut])
def search_bookings(
    q: str,
    db: Session = Depends(get_db)
):
    q_lower = f"%{q.lower()}%"

    results = db.query(Booking).filter(
        (Booking.customer_name.ilike(q_lower)) |
        (Booking.license_plate.ilike(q_lower)) |
        (Booking.portal.ilike(q_lower))
    ).all()

    return results
