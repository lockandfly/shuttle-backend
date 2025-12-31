from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.bookings.models_orm import Booking
from app.bookings.schemas import BookingCreate, BookingUpdate
from app.pricing.service import calculate_dynamic_price


# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------

def create_booking(db: Session, data: BookingCreate):
    # Dynamic Pricing
    duration_days = (data.departure_time - data.arrival_time).days

    pricing = calculate_dynamic_price(
        db=db,
        base_price=data.base_price,
        arrival_date=data.arrival_time.isoformat(),
        stay_length=duration_days,
        portal=data.portal.value if data.portal else "direct",
    )

    booking = Booking(
        customer_name=data.customer_name,
        customer_phone=data.customer_phone,
        license_plate=data.license_plate,
        arrival_time=data.arrival_time,
        departure_time=data.departure_time,

        portal=data.portal.value if data.portal else "direct",
        parking_area=data.parking_area,
        passenger_count=data.passenger_count,

        base_price=pricing["base_price"],
        final_price=pricing["final_price"],
        pricing_breakdown=pricing["adjustments"],
        pricing_reasoning=pricing["reasoning"],
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


# ---------------------------------------------------------
# LIST
# ---------------------------------------------------------

def list_bookings(db: Session):
    return db.query(Booking).all()


# ---------------------------------------------------------
# GET SINGLE
# ---------------------------------------------------------

def get_booking(db: Session, booking_id: int):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


# ---------------------------------------------------------
# UPDATE
# ---------------------------------------------------------

def update_booking(db: Session, booking_id: int, data: BookingUpdate):
    booking = get_booking(db, booking_id)

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(booking, field, value)

    db.commit()
    db.refresh(booking)
    return booking


# ---------------------------------------------------------
# DELETE
# ---------------------------------------------------------

def delete_booking(db: Session, booking_id: int):
    booking = get_booking(db, booking_id)
    db.delete(booking)
    db.commit()
    return {"deleted": True}
