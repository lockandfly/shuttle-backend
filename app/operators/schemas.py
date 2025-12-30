from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------

class OperatorCreate(BaseModel):
    name: str
    role: str
    phone: Optional[str] = None


# ---------------------------------------------------------
# UPDATE
# ---------------------------------------------------------

class OperatorUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    phone: Optional[str] = None


# ---------------------------------------------------------
# READ
# ---------------------------------------------------------

class OperatorRead(BaseModel):
    id: int
    name: str
    role: str
    phone: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
