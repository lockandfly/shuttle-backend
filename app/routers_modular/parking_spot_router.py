from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.parking.schemas import (
    ParkingSpotCreate,
    ParkingSpotUpdate,
    ParkingSpotRead,
)
from app.parking.models_orm import SpotStatus
from app.parking import service

router = APIRouter(tags=["Parking Spots"])


@router.post(
    "/",
    response_model=ParkingSpotRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new parking spot",
    description="Creates a new parking spot inside an existing parking area."
)
def create_spot(
    data: ParkingSpotCreate,
    db: Session = Depends(get_db),
):
    if data.spot_number <= 0:
        raise HTTPException(status_code=400, detail="Spot number must be positive")

    try:
        return service.create_spot(db, data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/",
    response_model=list[ParkingSpotRead],
    summary="List all parking spots"
)
def list_spots(db: Session = Depends(get_db)):
    return service.list_spots(db)


@router.get(
    "/area/{area_id}",
    response_model=list[ParkingSpotRead],
    summary="List spots by area"
)
def list_spots_by_area(area_id: int, db: Session = Depends(get_db)):
    return service.list_spots_by_area(db, area_id)


@router.get(
    "/{spot_id}",
    response_model=ParkingSpotRead,
    summary="Get a parking spot"
)
def get_spot(spot_id: int, db: Session = Depends(get_db)):
    return service.get_spot(db, spot_id)


@router.patch(
    "/{spot_id}",
    response_model=ParkingSpotRead,
    summary="Update a parking spot"
)
def update_spot(
    spot_id: int,
    data: ParkingSpotUpdate,
    db: Session = Depends(get_db),
):
    return service.update_spot(db, spot_id, data)


@router.patch(
    "/{spot_id}/status",
    response_model=ParkingSpotRead,
    summary="Update spot status"
)
def update_status(
    spot_id: int,
    status: SpotStatus,
    db: Session = Depends(get_db),
):
    return service.update_status(db, spot_id, status)


@router.patch(
    "/{spot_id}/assign-booking/{booking_id}",
    response_model=ParkingSpotRead,
    summary="Assign booking to spot"
)
def assign_booking(
    spot_id: int,
    booking_id: int,
    db: Session = Depends(get_db),
):
    return service.assign_booking(db, spot_id, booking_id)


@router.patch(
    "/{spot_id}/release-booking",
    response_model=ParkingSpotRead,
    summary="Release booking from spot"
)
def release_booking(spot_id: int, db: Session = Depends(get_db)):
    return service.release_booking(db, spot_id)


@router.delete(
    "/{spot_id}",
    summary="Delete a parking spot"
)
def delete_spot(spot_id: int, db: Session = Depends(get_db)):
    return service.delete_spot(db, spot_id)
