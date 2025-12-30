from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.shuttle.schemas import (
    ShuttleCreate,
    ShuttleUpdate,
    ShuttleRead,
    ShuttleLogCreate,
    ShuttleLogRead,
    ShuttleMovementCreate,
    ShuttleMovementRead,
)
from app.shuttle import service

router = APIRouter(tags=["Shuttle"])


# ---------------------------------------------------------
# SHUTTLE MOVEMENTS (Tracking)
# ---------------------------------------------------------

@router.post(
    "/movements",
    response_model=ShuttleMovementRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register a shuttle movement",
    description="Creates a new shuttle movement entry for tracking operator activity."
)
def create_movement(
    data: ShuttleMovementCreate,
    db: Session = Depends(get_db)
):
    try:
        return service.create_movement(db, data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/movements",
    response_model=list[ShuttleMovementRead],
    summary="List shuttle movements",
    description="Returns all shuttle movements, optionally filtered by operator ID."
)
def list_movements(
    operator_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db)
):
    try:
        return service.list_movements(db, operator_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------
# SHUTTLE LOGS
# ---------------------------------------------------------

@router.post(
    "/logs",
    response_model=ShuttleLogRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a shuttle log entry",
    description="Registers a new log entry for a shuttle (e.g., maintenance, notes)."
)
def create_log(
    data: ShuttleLogCreate,
    db: Session = Depends(get_db)
):
    try:
        return service.create_log(db, data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/logs",
    response_model=list[ShuttleLogRead],
    summary="List shuttle logs",
    description="Returns all shuttle logs, optionally filtered by shuttle ID."
)
def list_logs(
    shuttle_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db)
):
    try:
        return service.list_logs(db, shuttle_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------
# SHUTTLES (CRUD)
# ---------------------------------------------------------

@router.post(
    "/",
    response_model=ShuttleRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new shuttle",
    description="Registers a new shuttle with name, plate, and capacity."
)
def create_shuttle(
    data: ShuttleCreate,
    db: Session = Depends(get_db)
):
    if data.capacity <= 0:
        raise HTTPException(status_code=400, detail="Capacity must be positive")

    try:
        return service.create_shuttle(db, data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/",
    response_model=list[ShuttleRead],
    summary="List all shuttles",
    description="Returns all registered shuttles."
)
def list_shuttles(db: Session = Depends(get_db)):
    try:
        return service.list_shuttles(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{shuttle_id}",
    response_model=ShuttleRead,
    summary="Get a shuttle",
    description="Returns details of a specific shuttle."
)
def get_shuttle(
    shuttle_id: int,
    db: Session = Depends(get_db)
):
    try:
        return service.get_shuttle(db, shuttle_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch(
    "/{shuttle_id}",
    response_model=ShuttleRead,
    summary="Update a shuttle",
    description="Updates fields of a shuttle using partial update."
)
def update_shuttle(
    shuttle_id: int,
    data: ShuttleUpdate,
    db: Session = Depends(get_db)
):
    try:
        return service.update_shuttle(db, shuttle_id, data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/{shuttle_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a shuttle",
    description="Deletes a shuttle and returns a confirmation object."
)
def delete_shuttle(
    shuttle_id: int,
    db: Session = Depends(get_db)
):
    try:
        return service.delete_shuttle(db, shuttle_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
