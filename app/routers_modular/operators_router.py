from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.operators.schemas import (
    OperatorCreate,
    OperatorRead,
    OperatorUpdate,
)
from app.operators.service import (
    list_operators,
    create_operator,
    get_operator,
    update_operator,
    delete_operator,
)

router = APIRouter(
    prefix="",
    tags=["Operators"]
)

# LIST OPERATORS
@router.get("/", response_model=list[OperatorRead])
def list_all_operators(db: Session = Depends(get_db)):
    return list_operators(db)


# CREATE OPERATOR
@router.post("/", response_model=OperatorRead)
def create_new_operator(payload: OperatorCreate, db: Session = Depends(get_db)):
    return create_operator(db, payload)


# GET OPERATOR BY ID
@router.get("/{operator_id}", response_model=OperatorRead)
def get_single_operator(operator_id: int, db: Session = Depends(get_db)):
    operator = get_operator(db, operator_id)
    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")
    return operator


# UPDATE OPERATOR
@router.patch("/{operator_id}", response_model=OperatorRead)
def update_single_operator(operator_id: int, payload: OperatorUpdate, db: Session = Depends(get_db)):
    return update_operator(db, operator_id, payload)


# DELETE OPERATOR
@router.delete("/{operator_id}")
def delete_single_operator(operator_id: int, db: Session = Depends(get_db)):
    delete_operator(db, operator_id)
    return {"status": "deleted"}
