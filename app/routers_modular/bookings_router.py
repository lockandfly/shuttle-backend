from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.bookings.schemas import BookingCreate, BookingRead, BookingUpdate
from app.bookings.service import (
    create_booking,
    list_bookings,
    get_booking,
    update_booking,
    delete_booking,
)

router = APIRouter(
    prefix="",
    tags=["Bookings"]
)

@router.get("/", response_model=list[BookingRead])
def list_all_bookings(db: Session = Depends(get_db)):
    return list_bookings(db)


@router.post("/", response_model=BookingRead)
def create_new_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    return create_booking(db, payload)


@router.get("/{booking_id}", response_model=BookingRead)
def get_single_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.put("/{booking_id}", response_model=BookingRead)
def update_existing_booking(booking_id: int, payload: BookingUpdate, db: Session = Depends(get_db)):
    return update_booking(db, booking_id, payload)


@router.delete("/{booking_id}")
def delete_existing_booking(booking_id: int, db: Session = Depends(get_db)):
    delete_booking(db, booking_id)
    return {"status": "deleted"}
