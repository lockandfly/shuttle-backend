from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.pricing.schemas import PricingRequest, PricingResponse
from app.pricing.service import calculate_dynamic_price

router = APIRouter(prefix="/pricing", tags=["Dynamic Pricing"])


@router.post("/calculate", response_model=PricingResponse)
def calculate_price(data: PricingRequest, db: Session = Depends(get_db)):
    """
    Calcola il prezzo dinamico in base alle regole presenti nel database.
    """
    result = calculate_dynamic_price(
        db=db,
        base_price=data.base_price,
        arrival_date=data.arrival_date,
        stay_length=data.stay_length,
        portal=data.portal,
    )
    return result
