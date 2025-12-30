from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.operators.models_orm import Operator
from app.operators.schemas import OperatorCreate, OperatorUpdate


# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------

def create_operator(db: Session, data: OperatorCreate):
    operator = Operator(**data.model_dump())
    db.add(operator)
    db.commit()
    db.refresh(operator)
    return operator


# ---------------------------------------------------------
# LIST
# ---------------------------------------------------------

def list_operators(db: Session):
    return db.query(Operator).all()


# ---------------------------------------------------------
# GET SINGLE
# ---------------------------------------------------------

def get_operator(db: Session, operator_id: int):
    operator = db.query(Operator).filter(Operator.id == operator_id).first()
    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")
    return operator


# ---------------------------------------------------------
# UPDATE
# ---------------------------------------------------------

def update_operator(db: Session, operator_id: int, data: OperatorUpdate):
    operator = get_operator(db, operator_id)

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(operator, field, value)

    db.commit()
    db.refresh(operator)
    return operator


# ---------------------------------------------------------
# DELETE
# ---------------------------------------------------------

def delete_operator(db: Session, operator_id: int):
    operator = get_operator(db, operator_id)
    db.delete(operator)
    db.commit()
    return {"deleted": True}
