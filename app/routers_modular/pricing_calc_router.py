from fastapi import APIRouter
from datetime import datetime

from app.bookings.services.pricing_service import PricingService

router = APIRouter(prefix="/pricing", tags=["Dynamic Pricing"])


@router.post("/calc")
def calculate_dynamic_price(
    arrival_time: datetime,
    departure_time: datetime,
    passenger_count: int = 1,
    portal: str = "direct",
    parking_area: str = "standard"
):
    """
    Calcolo base del prezzo dinamico (Livello 1).
    """

    result = PricingService.calculate_price(
        arrival_time=arrival_time,
        departure_time=departure_time,
        passenger_count=passenger_count,
        portal=portal,
        parking_area=parking_area
    )

    return result
