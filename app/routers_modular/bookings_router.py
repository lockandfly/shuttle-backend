from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.bookings.schemas import BookingCreate, BookingUpdate, BookingRead
from app.bookings import service

router = APIRouter(tags=["Bookings"])


@router.post(
    "/",
    response_model=BookingRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new booking"
)
def create_booking(
    data: BookingCreate,
    db: Session = Depends(get_db),
):
    if not data.customer_name.strip():
        raise HTTPException(status_code=400, detail="Customer name cannot be empty")

    try:
        return service.create_booking(db, data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/",
    response_model=list[BookingRead],
    summary="List all bookings"
)
def list_bookings(db: Session = Depends(get_db)):
    return service.list_bookings(db)


@router.get(
    "/{booking_id}",
    response_model=BookingRead,
    summary="Get a booking"
)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    return service.get_booking(db, booking_id)


@router.patch(
    "/{booking_id}",
    response_model=BookingRead,
    summary="Update a booking"
)
def update_booking(
    booking_id: int,
    data: BookingUpdate,
    db: Session = Depends(get_db),
):
    return service.update_booking(db, booking_id, data)


@router.delete(
    "/{booking_id}",
    summary="Delete a booking"
)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    return service.delete_booking(db, booking_id)
