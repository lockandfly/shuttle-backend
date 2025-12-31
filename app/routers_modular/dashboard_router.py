from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dashboard.service import get_dashboard_data

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

# ---------------------------------------------------------
# AGGREGATED DASHBOARD DATA
# ---------------------------------------------------------

@router.get(
    "/aggregated",
    status_code=status.HTTP_200_OK,
    summary="Get aggregated dashboard data"
)
def get_aggregated_dashboard(db: Session = Depends(get_db)):
    try:
        return get_dashboard_data(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
