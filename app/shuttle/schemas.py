from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ---------------------------------------------------------
# SHUTTLE (CRUD)
# ---------------------------------------------------------

class ShuttleBase(BaseModel):
    name: str
    plate: str
    capacity: int


class ShuttleCreate(ShuttleBase):
    pass


class ShuttleUpdate(BaseModel):
    name: Optional[str] = None
    plate: Optional[str] = None
    capacity: Optional[int] = None


class ShuttleRead(ShuttleBase):
    id: int

    model_config = {
        "from_attributes": True
    }


# ---------------------------------------------------------
# SHUTTLE LOGS
# ---------------------------------------------------------

class ShuttleLogCreate(BaseModel):
    shuttle_id: int
    message: str


class ShuttleLogRead(BaseModel):
    id: int
    shuttle_id: int
    message: str
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }


# ---------------------------------------------------------
# SHUTTLE MOVEMENTS (Tracking)
# ---------------------------------------------------------

class ShuttleMovementCreate(BaseModel):
    shuttle_id: int
    operator_id: int
    action: str  # "depart" | "arrive"
    notes: Optional[str] = None


class ShuttleMovementRead(BaseModel):
    id: int
    shuttle_id: int
    operator_id: int
    action: str
    notes: Optional[str]
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }
