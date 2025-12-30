from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.parking.models_orm import SpotStatus


# ---------------------------------------------------------
# PARKING AREA SCHEMAS
# ---------------------------------------------------------

class ParkingAreaCreate(BaseModel):
    name: str
    total_spots: Optional[int] = None
    description: Optional[str] = None


class ParkingAreaRead(BaseModel):
    id: int
    name: str
    total_spots: Optional[int] = None
    description: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


# ---------------------------------------------------------
# PARKING SPOT SCHEMAS
# ---------------------------------------------------------

class ParkingSpotBase(BaseModel):
    area_id: int
    spot_number: str
    status: SpotStatus = SpotStatus.FREE
    x: Optional[float] = None
    y: Optional[float] = None
    keyslot_id: Optional[int] = None
    booking_id: Optional[int] = None


class ParkingSpotCreate(ParkingSpotBase):
    pass


class ParkingSpotUpdate(BaseModel):
    spot_number: Optional[str] = None
    status: Optional[SpotStatus] = None
    x: Optional[float] = None
    y: Optional[float] = None
    keyslot_id: Optional[int] = None
    booking_id: Optional[int] = None


class ParkingSpotRead(ParkingSpotBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
