from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.bookings.models_orm import Booking
from app.bookings.schemas_bookings import BookingResponse

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.get("/", response_model=list[BookingResponse])
def get_all_bookings(db: Session = Depends(get_db)):
    try:
        return db.query(Booking).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    try:
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        return booking
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
