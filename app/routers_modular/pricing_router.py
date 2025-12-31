from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.pricing.schemas import PricingRequest, PricingResponse
from app.pricing.service import calculate_dynamic_price

router = APIRouter(
    prefix="",
    tags=["Pricing"]
)

@router.post("/calculate", response_model=PricingResponse)
def calculate_price(payload: PricingRequest, db: Session = Depends(get_db)):
    """
    Calcola il prezzo dinamico in base a:
    - base price
    - arrival date
    - stay length
    - portal
    """
    return calculate_dynamic_price(
        db=db,
        base_price=payload.base_price,
        arrival_date=payload.arrival_date,
        stay_length=payload.stay_length,
        portal=payload.portal,
    )
