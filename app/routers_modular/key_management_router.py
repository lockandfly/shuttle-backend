from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.key_management.schemas import (
    KeySlotCreate,
    KeySlotUpdate,
    KeySlotRead,
    KeyMovementCreate,
    KeyMovementRead,
)
from app.key_management.service import (
    create_keyslot,
    list_keyslots,
    get_keyslot,
    update_keyslot,
    delete_keyslot,
    create_movement,
    list_movements,
)

router = APIRouter(
    prefix="",
    tags=["Key Management"]
)

# ---------------------------------------------------------
# KEY SLOTS
# ---------------------------------------------------------

@router.get("/slots", response_model=list[KeySlotRead])
def get_all_keyslots(db: Session = Depends(get_db)):
    return list_keyslots(db)


@router.post("/slots", response_model=KeySlotRead)
def create_new_keyslot(payload: KeySlotCreate, db: Session = Depends(get_db)):
    return create_keyslot(db, payload)


@router.get("/slots/{slot_id}", response_model=KeySlotRead)
def get_single_keyslot(slot_id: int, db: Session = Depends(get_db)):
    return get_keyslot(db, slot_id)


@router.patch("/slots/{slot_id}", response_model=KeySlotRead)
def update_single_keyslot(slot_id: int, payload: KeySlotUpdate, db: Session = Depends(get_db)):
    return update_keyslot(db, slot_id, payload)


@router.delete("/slots/{slot_id}")
def delete_single_keyslot(slot_id: int, db: Session = Depends(get_db)):
    return delete_keyslot(db, slot_id)


# ---------------------------------------------------------
# KEY MOVEMENTS
# ---------------------------------------------------------

@router.post("/movements", response_model=KeyMovementRead)
def create_key_movement(payload: KeyMovementCreate, db: Session = Depends(get_db)):
    return create_movement(db, payload)


@router.get("/movements", response_model=list[KeyMovementRead])
def get_key_movements(slot_id: int | None = None, db: Session = Depends(get_db)):
    return list_movements(db, slot_id=slot_id)
