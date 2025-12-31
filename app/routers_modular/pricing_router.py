from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.bookings.models_orm import Booking   # ← IMPORT CORRETTO
from app.bookings.schemas_pricing import PricingCreate, PricingOut, PricingUpdate

router = APIRouter(prefix="/pricing", tags=["Dynamic Pricing"])


# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------
@router.post("/", response_model=PricingOut)
def create_pricing(data: PricingCreate, db: Session = Depends(get_db)):
    booking = Booking(**data.dict())
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


# ---------------------------------------------------------
# READ ALL
# ---------------------------------------------------------
@router.get("/", response_model=list[PricingOut])
def get_all_pricing(db: Session = Depends(get_db)):
    return db.query(Booking).all()


# ---------------------------------------------------------
# READ ONE
# ---------------------------------------------------------
@router.get("/{booking_id}", response_model=PricingOut)
def get_pricing(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")
    return booking


# ---------------------------------------------------------
# UPDATE
# ---------------------------------------------------------
@router.patch("/{booking_id}", response_model=PricingOut)
def update_pricing(booking_id: int, data: PricingUpdate, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(booking, key, value)

    db.commit()
    db.refresh(booking)
    return booking


# ---------------------------------------------------------
# DELETE
# ---------------------------------------------------------
@router.delete("/{booking_id}")
def delete_pricing(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")

    db.delete(booking)
    db.commit()

    return {"status": "deleted", "id": booking_id}
