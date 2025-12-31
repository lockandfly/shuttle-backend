from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.key_management.models_orm import KeySlot, KeyMovement
from app.key_management.schemas import (
    KeySlotCreate,
    KeySlotUpdate,
    KeyMovementCreate
)


# ---------------------------------------------------------
# KEYSLOTS
# ---------------------------------------------------------

def create_keyslot(db: Session, data: KeySlotCreate):
    """
    Create a new key slot.
    """
    slot = KeySlot(**data.model_dump())
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot


def list_keyslots(db: Session):
    return db.query(KeySlot).order_by(KeySlot.id).all()


def get_keyslot(db: Session, slot_id: int):
    slot = db.query(KeySlot).filter(KeySlot.id == slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Key slot not found")
    return slot


def update_keyslot(db: Session, slot_id: int, data: KeySlotUpdate):
    slot = get_keyslot(db, slot_id)

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(slot, field, value)

    db.commit()
    db.refresh(slot)
    return slot


def delete_keyslot(db: Session, slot_id: int):
    slot = get_keyslot(db, slot_id)
    db.delete(slot)
    db.commit()
    return {"status": "success", "deleted": True, "slot_id": slot_id}


# ---------------------------------------------------------
# KEY MOVEMENTS
# ---------------------------------------------------------

def create_movement(db: Session, data: KeyMovementCreate):
    """
    Register a key movement (pickup/return).
    """
    slot = get_keyslot(db, data.keyslot_id)

    movement = KeyMovement(**data.model_dump())
    db.add(movement)
    db.commit()
    db.refresh(movement)
    return movement


def list_movements(db: Session, slot_id: int | None = None):
    query = db.query(KeyMovement)

    if slot_id is not None:
        query = query.filter(KeyMovement.keyslot_id == slot_id)

    return query.order_by(KeyMovement.timestamp.desc()).all()
