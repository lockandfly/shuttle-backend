from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.parking.service import create_area, list_areas
from app.parking.schemas import ParkingAreaCreate, ParkingAreaRead

router = APIRouter(tags=["Parking Areas"])


@router.post(
    "/areas",
    response_model=ParkingAreaRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new parking area",
    description="Creates a new parking area with a validated name and optional description."
)
def create_parking_area(
    area: ParkingAreaCreate,
    db: Session = Depends(get_db),
):
    # Validazione minima lato router (micro-ottimizzazione)
    if not area.name or area.name.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The parking area name cannot be empty."
        )

    try:
        return create_area(db, area)
    except Exception as e:
        # Error handling essenziale
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating parking area: {str(e)}"
        )


@router.get(
    "/areas",
    response_model=list[ParkingAreaRead],
    summary="List all parking areas",
    description="Returns all parking areas stored in the system."
)
def get_parking_areas(db: Session = Depends(get_db)):
    try:
        return list_areas(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving parking areas: {str(e)}"
        )
