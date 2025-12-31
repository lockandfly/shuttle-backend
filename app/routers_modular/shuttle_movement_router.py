from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.shuttle.schemas import (
    ShuttleMovementCreate,
    ShuttleMovementRead,
    ShuttleLogCreate,
    ShuttleLogRead,
)
from app.shuttle.service import (
    create_movement,
    list_movements,
    create_log,
    list_logs,
)

router = APIRouter(
    prefix="",
    tags=["Shuttle Movements"]
)

# CREATE MOVEMENT
@router.post("/", response_model=ShuttleMovementRead)
def register_movement(payload: ShuttleMovementCreate, db: Session = Depends(get_db)):
    return create_movement(db, payload)


# LIST MOVEMENTS (con filtri opzionali)
@router.get("/", response_model=list[ShuttleMovementRead])
def get_movements(
    shuttle_id: int | None = None,
    operator_id: int | None = None,
    action: str | None = None,
    db: Session = Depends(get_db),
):
    return list_movements(
        db=db,
        shuttle_id=shuttle_id,
        operator_id=operator_id,
        action=action,
    )


# CREATE LOG
@router.post("/logs", response_model=ShuttleLogRead)
def register_log(payload: ShuttleLogCreate, db: Session = Depends(get_db)):
    return create_log(db, payload)


# LIST LOGS (con filtro opzionale per shuttle)
@router.get("/logs", response_model=list[ShuttleLogRead])
def get_logs(
    shuttle_id: int | None = None,
    db: Session = Depends(get_db),
):
    return list_logs(db, shuttle_id=shuttle_id)
