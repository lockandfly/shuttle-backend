from sqlalchemy.orm import Session
from . import models, schemas

def create_booking(db: Session, booking: schemas.BookingCreate):
    db_booking = models.Booking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).offset(skip).limit(limit).all()

def get_booking_by_email(db: Session, email: str):
    return db.query(models.Booking).filter(models.Booking.email == email).first()

def delete_all_bookings(db: Session):
    db.query(models.Booking).delete()
    db.commit()
