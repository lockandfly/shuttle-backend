from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.parking.models_orm import ParkingArea, ParkingSpot, SpotStatus
from app.parking.schemas import ParkingAreaCreate, ParkingSpotCreate, ParkingSpotUpdate
from app.bookings.models_orm import Booking


# ---------------------------------------------------------
# PARKING AREA SERVICE
# ---------------------------------------------------------

def create_area(db: Session, data: ParkingAreaCreate):
    """
    Create a parking area.
    Adds minimal validation and ensures consistent error handling.
    """
    # Optional: prevent duplicate area names
    existing = db.query(ParkingArea).filter(ParkingArea.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="A parking area with this name already exists")

    area = ParkingArea(**data.model_dump())
    db.add(area)
    db.commit()
    db.refresh(area)
    return area


def list_areas(db: Session):
    """Return all parking areas."""
    return db.query(ParkingArea).order_by(ParkingArea.id).all()


# ---------------------------------------------------------
# PARKING SPOT SERVICE
# ---------------------------------------------------------

def create_spot(db: Session, data: ParkingSpotCreate):
    """
    Create a parking spot inside an existing area.
    Includes duplicate checks and consistent error messages.
    """
    area = db.query(ParkingArea).filter(ParkingArea.id == data.area_id).first()
    if not area:
        raise HTTPException(status_code=404, detail="Parking area not found")

    # Prevent duplicate spot numbers within the same area
    existing = (
        db.query(ParkingSpot)
        .filter(
            ParkingSpot.area_id == data.area_id,
            ParkingSpot.spot_number == data.spot_number
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Spot number already exists in this area")

    spot = ParkingSpot(**data.model_dump())
    db.add(spot)
    db.commit()
    db.refresh(spot)
    return spot


def list_spots(db: Session):
    """Return all parking spots."""
    return db.query(ParkingSpot).order_by(ParkingSpot.area_id, ParkingSpot.spot_number).all()


def list_spots_by_area(db: Session, area_id: int):
    """Return all spots belonging to a specific area."""
    return (
        db.query(ParkingSpot)
        .filter(ParkingSpot.area_id == area_id)
        .order_by(ParkingSpot.spot_number)
        .all()
    )


def get_spot(db: Session, spot_id: int):
    """Return a single spot or raise 404."""
    spot = db.query(ParkingSpot).filter(ParkingSpot.id == spot_id).first()
    if not spot:
        raise HTTPException(status_code=404, detail="Parking spot not found")
    return spot


def update_spot(db: Session, spot_id: int, data: ParkingSpotUpdate):
    """
    Update a parking spot.
    Uses exclude_unset to avoid overwriting fields unintentionally.
    """
    spot = get_spot(db, spot_id)

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(spot, field, value)

    db.commit()
    db.refresh(spot)
    return spot


def update_status(db: Session, spot_id: int, status: SpotStatus):
    """Update only the status of a parking spot."""
    spot = get_spot(db, spot_id)
    spot.status = status
    db.commit()
    db.refresh(spot)
    return spot


# ---------------------------------------------------------
# BOOKING ASSIGNMENT
# ---------------------------------------------------------

def assign_booking(db: Session, spot_id: int, booking_id: int):
    """
    Assign a booking to a spot.
    Ensures the spot is free and the booking exists.
    """
    spot = get_spot(db, spot_id)

    if spot.status != SpotStatus.FREE:
        raise HTTPException(status_code=400, detail="Spot is not free")

    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    spot.booking_id = booking_id
    spot.status = SpotStatus.OCCUPIED

    db.commit()
    db.refresh(spot)
    return spot


def release_booking(db: Session, spot_id: int):
    """
    Release a spot from its booking.
    Sets status back to FREE.
    """
    spot = get_spot(db, spot_id)
    spot.booking_id = None
    spot.status = SpotStatus.FREE

    db.commit()
    db.refresh(spot)
    return spot


def delete_spot(db: Session, spot_id: int):
    """
    Delete a parking spot.
    Returns a consistent response object.
    """
    spot = get_spot(db, spot_id)
    db.delete(spot)
    db.commit()
    return {"status": "success", "deleted": True, "spot_id": spot_id}
