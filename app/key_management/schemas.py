from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ---------------------------------------------------------
# KEYSLOT
# ---------------------------------------------------------

class KeySlotCreate(BaseModel):
    label: str
    description: Optional[str] = None


class KeySlotUpdate(BaseModel):
    label: Optional[str] = None
    description: Optional[str] = None


class KeySlotRead(BaseModel):
    id: int
    label: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


# ---------------------------------------------------------
# KEY MOVEMENT
# ---------------------------------------------------------

class KeyMovementCreate(BaseModel):
    keyslot_id: int
    operator_name: str
    action: str  # "pickup" | "return"


class KeyMovementRead(BaseModel):
    id: int
    keyslot_id: int
    operator_name: str
    action: str
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }
