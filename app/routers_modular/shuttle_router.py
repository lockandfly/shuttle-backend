from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.shuttle.schemas import (
    ShuttleCreate,
    ShuttleUpdate,
    ShuttleRead,
)
from app.shuttle.service import (
    create_shuttle,
    list_shuttles,
    get_shuttle,
    update_shuttle,
    delete_shuttle,
)

router = APIRouter(
    prefix="",
    tags=["Shuttle"]
)

# LIST SHUTTLES
@router.get("/", response_model=list[ShuttleRead])
def list_all_shuttles(db: Session = Depends(get_db)):
    return list_shuttles(db)


# CREATE SHUTTLE
@router.post("/", response_model=ShuttleRead)
def create_new_shuttle(payload: ShuttleCreate, db: Session = Depends(get_db)):
    return create_shuttle(db, payload)


# GET SINGLE SHUTTLE
@router.get("/{shuttle_id}", response_model=ShuttleRead)
def get_single_shuttle(shuttle_id: int, db: Session = Depends(get_db)):
    return get_shuttle(db, shuttle_id)


# UPDATE SHUTTLE
@router.patch("/{shuttle_id}", response_model=ShuttleRead)
def update_single_shuttle(shuttle_id: int, payload: ShuttleUpdate, db: Session = Depends(get_db)):
    return update_shuttle(db, shuttle_id, payload)


# DELETE SHUTTLE
@router.delete("/{shuttle_id}")
def delete_single_shuttle(shuttle_id: int, db: Session = Depends(get_db)):
    delete_shuttle(db, shuttle_id)
    return {"status": "deleted"}
