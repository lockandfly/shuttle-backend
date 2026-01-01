from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.bookings.schemas import BookingCreate, BookingRead, BookingUpdate
from app.bookings.service import (
    list_bookings,
    get_booking,
    create_booking,
    update_booking,
    delete_booking,
)

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/", response_model=list[BookingRead])
def get_all(db: Session = Depends(get_db)):
    return list_bookings(db)


@router.get("/{booking_id}", response_model=BookingRead)
def get_one(booking_id: int, db: Session = Depends(get_db)):
    return get_booking(db, booking_id)


@router.post("/", response_model=BookingRead)
def create(data: BookingCreate, db: Session = Depends(get_db)):
    return create_booking(db, data)


@router.put("/{booking_id}", response_model=BookingRead)
def update(booking_id: int, data: BookingUpdate, db: Session = Depends(get_db)):
    return update_booking(db, booking_id, data)


@router.delete("/{booking_id}")
def delete(booking_id: int, db: Session = Depends(get_db)):
    return delete_booking(db, booking_id)
