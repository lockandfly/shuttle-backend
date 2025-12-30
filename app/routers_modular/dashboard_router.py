from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dashboard.service import get_dashboard_data

router = APIRouter(tags=["Dashboard"])


@router.get(
    "/aggregated",
    status_code=status.HTTP_200_OK,
    summary="Get aggregated dashboard data",
    description=(
        "Returns the aggregated dashboard containing:\n"
        "- parking status\n"
        "- bookings status\n"
        "- shuttle status\n"
        "- key management status\n"
        "- operators\n"
        "- generation metadata"
    )
)
def get_aggregated_dashboard(db: Session = Depends(get_db)):
    try:
        return get_dashboard_data(db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving dashboard data: {str(e)}"
        )
