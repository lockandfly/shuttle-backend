from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.occupancy.schemas import OccupancyResponse
from app.occupancy.service import get_current_occupancy

router = APIRouter(
    prefix="",
    tags=["Occupancy"]
)


@router.get("/", response_model=OccupancyResponse)
def occupancy_status(db: Session = Depends(get_db)):
    return get_current_occupancy(db)
