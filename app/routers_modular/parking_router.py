from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.parking.schemas import ParkingAreaCreate, ParkingAreaRead
from app.parking.service import (
    create_area,
    list_areas,
)

router = APIRouter(
    prefix="/areas",
    tags=["Parking Areas"]
)

@router.get("/", response_model=list[ParkingAreaRead])
def get_all_areas(db: Session = Depends(get_db)):
    return list_areas(db)

@router.post("/", response_model=ParkingAreaRead)
def create_new_area(payload: ParkingAreaCreate, db: Session = Depends(get_db)):
    return create_area(db, payload)
