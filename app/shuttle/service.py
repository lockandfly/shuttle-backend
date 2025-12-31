from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.shuttle.models_orm import Shuttle, ShuttleLog, ShuttleMovement
from app.shuttle.schemas import (
    ShuttleCreate,
    ShuttleUpdate,
    ShuttleLogCreate,
    ShuttleMovementCreate,
)
from app.operators.models_orm import Operator


# ---------------------------------------------------------
# SHUTTLES (CRUD)
# ---------------------------------------------------------

def create_shuttle(db: Session, data: ShuttleCreate):
    shuttle = Shuttle(**data.model_dump())
    db.add(shuttle)
    db.commit()
    db.refresh(shuttle)
    return shuttle


def list_shuttles(db: Session):
    return db.query(Shuttle).all()


def get_shuttle(db: Session, shuttle_id: int):
    shuttle = db.query(Shuttle).filter(Shuttle.id == shuttle_id).first()
    if not shuttle:
        raise HTTPException(status_code=404, detail="Shuttle not found")
    return shuttle


def update_shuttle(db: Session, shuttle_id: int, data: ShuttleUpdate):
    shuttle = get_shuttle(db, shuttle_id)

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(shuttle, field, value)

    db.commit()
    db.refresh(shuttle)
    return shuttle


def delete_shuttle(db: Session, shuttle_id: int):
    shuttle = get_shuttle(db, shuttle_id)
    db.delete(shuttle)
    db.commit()
    return {"deleted": True}


# ---------------------------------------------------------
# SHUTTLE LOGS
# ---------------------------------------------------------

def create_log(db: Session, data: ShuttleLogCreate):
    log = ShuttleLog(**data.model_dump())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def list_logs(db: Session, shuttle_id: int | None = None):
    query = db.query(ShuttleLog)
    if shuttle_id:
        query = query.filter(ShuttleLog.shuttle_id == shuttle_id)
    return query.order_by(ShuttleLog.timestamp.desc()).all()


# ---------------------------------------------------------
# SHUTTLE MOVEMENTS (Tracking)
# ---------------------------------------------------------

def create_movement(db: Session, data: ShuttleMovementCreate):
    # Check shuttle exists
    shuttle = db.query(Shuttle).filter(Shuttle.id == data.shuttle_id).first()
    if not shuttle:
        raise HTTPException(status_code=404, detail="Shuttle not found")

    # Check operator exists
    operator = db.query(Operator).filter(Operator.id == data.operator_id).first()
    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")

    movement = ShuttleMovement(**data.model_dump())
    db.add(movement)
    db.commit()
    db.refresh(movement)
    return movement


def list_movements(
    db: Session,
    shuttle_id: int | None = None,
    operator_id: int | None = None,
    action: str | None = None
):
    query = db.query(ShuttleMovement)

    if shuttle_id:
        query = query.filter(ShuttleMovement.shuttle_id == shuttle_id)

    if operator_id:
        query = query.filter(ShuttleMovement.operator_id == operator_id)

    if action:
        query = query.filter(ShuttleMovement.action == action)

    return query.order_by(ShuttleMovement.timestamp.desc()).all()
