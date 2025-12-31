from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.parking.schemas import (
    ParkingSpotCreate,
    ParkingSpotUpdate,
    ParkingSpotRead,
)
from app.parking.service import (
    create_spot,
    list_spots,
    list_spots_by_area,
    get_spot,
    update_spot,
    update_status,
    assign_booking,
    release_booking,
    delete_spot,
)
from app.parking.models_orm import SpotStatus

router = APIRouter(
    prefix="/spots",
    tags=["Parking Spots"]
)

@router.get("/", response_model=list[ParkingSpotRead])
def get_all_spots(db: Session = Depends(get_db)):
    return list_spots(db)

@router.get("/area/{area_id}", response_model=list[ParkingSpotRead])
def get_spots_in_area(area_id: int, db: Session = Depends(get_db)):
    return list_spots_by_area(db, area_id)

@router.post("/", response_model=ParkingSpotRead)
def create_new_spot(payload: ParkingSpotCreate, db: Session = Depends(get_db)):
    return create_spot(db, payload)

@router.get("/{spot_id}", response_model=ParkingSpotRead)
def get_single_spot(spot_id: int, db: Session = Depends(get_db)):
    return get_spot(db, spot_id)

@router.patch("/{spot_id}", response_model=ParkingSpotRead)
def update_single_spot(spot_id: int, payload: ParkingSpotUpdate, db: Session = Depends(get_db)):
    return update_spot(db, spot_id, payload)

@router.patch("/{spot_id}/status/{status}", response_model=ParkingSpotRead)
def update_spot_status(spot_id: int, status: SpotStatus, db: Session = Depends(get_db)):
    return update_status(db, spot_id, status)

@router.post("/{spot_id}/assign/{booking_id}", response_model=ParkingSpotRead)
def assign_booking_to_spot(spot_id: int, booking_id: int, db: Session = Depends(get_db)):
    return assign_booking(db, spot_id, booking_id)

@router.post("/{spot_id}/release", response_model=ParkingSpotRead)
def release_spot_booking(spot_id: int, db: Session = Depends(get_db)):
    return release_booking(db, spot_id)

@router.delete("/{spot_id}")
def delete_single_spot(spot_id: int, db: Session = Depends(get_db)):
    return delete_spot(db, spot_id)
