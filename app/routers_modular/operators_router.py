from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.operators.schemas import OperatorCreate, OperatorUpdate, OperatorRead
from app.operators import service

router = APIRouter(tags=["Operators"])


# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------

@router.post(
    "/",
    response_model=OperatorRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new operator",
    description="Registers a new operator with name, role, and optional metadata."
)
def create_operator(
    data: OperatorCreate,
    db: Session = Depends(get_db),
):
    # Validazione minima lato router
    if not data.name or data.name.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Operator name cannot be empty."
        )

    try:
        return service.create_operator(db, data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating operator: {str(e)}"
        )


# ---------------------------------------------------------
# LIST
# ---------------------------------------------------------

@router.get(
    "/",
    response_model=list[OperatorRead],
    summary="List all operators",
    description="Returns all operators registered in the system."
)
def list_operators(db: Session = Depends(get_db)):
    try:
        return service.list_operators(db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving operators: {str(e)}"
        )


# ---------------------------------------------------------
# GET SINGLE
# ---------------------------------------------------------

@router.get(
    "/{operator_id}",
    response_model=OperatorRead,
    summary="Get an operator",
    description="Returns details of a specific operator."
)
def get_operator(
    operator_id: int,
    db: Session = Depends(get_db),
):
    try:
        return service.get_operator(db, operator_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving operator: {str(e)}"
        )


# ---------------------------------------------------------
# UPDATE
# ---------------------------------------------------------

@router.patch(
    "/{operator_id}",
    response_model=OperatorRead,
    summary="Update an operator",
    description="Updates fields of an operator using partial update."
)
def update_operator(
    operator_id: int,
    data: OperatorUpdate,
    db: Session = Depends(get_db),
):
    try:
        return service.update_operator(db, operator_id, data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error updating operator: {str(e)}"
        )


# ---------------------------------------------------------
# DELETE
# ---------------------------------------------------------

@router.delete(
    "/{operator_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an operator",
    description="Deletes an operator and returns a confirmation object."
)
def delete_operator(
    operator_id: int,
    db: Session = Depends(get_db),
):
    try:
        return service.delete_operator(db, operator_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting operator: {str(e)}"
        )
