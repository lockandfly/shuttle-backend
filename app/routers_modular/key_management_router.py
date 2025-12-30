from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.key_management.schemas import (
    KeySlotCreate,
    KeySlotUpdate,
    KeySlotRead,
    KeyMovementCreate,
    KeyMovementRead,
)
from app.key_management import service

router = APIRouter(tags=["Key Management"])


# ---------------------------------------------------------
# KEYSLOTS
# ---------------------------------------------------------

@router.post(
    "/slots",
    response_model=KeySlotRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new key slot",
    description="Creates a new key slot with a unique slot number."
)
def create_keyslot(
    data: KeySlotCreate,
    db: Session = Depends(get_db),
):
    if data.slot_number <= 0:
        raise HTTPException(status_code=400, detail="Slot number must be positive")

    try:
        return service.create_keyslot(db, data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/slots",
    response_model=list[KeySlotRead],
    summary="List all key slots"
)
def list_keyslots(db: Session = Depends(get_db)):
    return service.list_keyslots(db)


@router.get(
    "/slots/{slot_id}",
    response_model=KeySlotRead,
    summary="Get a key slot"
)
def get_keyslot(slot_id: int, db: Session = Depends(get_db)):
    return service.get_keyslot(db, slot_id)


@router.patch(
    "/slots/{slot_id}",
    response_model=KeySlotRead,
    summary="Update a key slot"
)
def update_keyslot(
    slot_id: int,
    data: KeySlotUpdate,
    db: Session = Depends(get_db),
):
    return service.update_keyslot(db, slot_id, data)


@router.delete(
    "/slots/{slot_id}",
    summary="Delete a key slot"
)
def delete_keyslot(slot_id: int, db: Session = Depends(get_db)):
    return service.delete_keyslot(db, slot_id)


# ---------------------------------------------------------
# KEY MOVEMENTS
# ---------------------------------------------------------

@router.post(
    "/movements",
    response_model=KeyMovementRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register a key movement"
)
def create_movement(
    data: KeyMovementCreate,
    db: Session = Depends(get_db),
):
    try:
        return service.create_movement(db, data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/movements",
    response_model=list[KeyMovementRead],
    summary="List key movements"
)
def list_movements(
    slot_id: int | None = None,
    db: Session = Depends(get_db),
):
    return service.list_movements(db, slot_id)
