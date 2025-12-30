from fastapi import APIRouter
from app.services.occupancy_service import (
    get_basic_occupancy,
    get_advanced_occupancy,
    get_advanced2_occupancy
)

router = APIRouter(prefix="/occupancy", tags=["Occupancy"])


@router.get("/basic")
def occupancy_basic():
    return get_basic_occupancy()


@router.get("/advanced")
def occupancy_advanced():
    return get_advanced_occupancy()


@router.get("/advanced2")
def occupancy_advanced2():
    return get_advanced2_occupancy()
