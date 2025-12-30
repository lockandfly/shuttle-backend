from datetime import datetime
from fastapi import HTTPException

from app.database import SessionLocal
from app.operators.models_orm import Operator, OperatorShift, OperatorActivity


# -------------------------
# LOGIN
# -------------------------

def operator_login(username: str, password: str):
    db = SessionLocal()
    try:
        op = db.query(Operator).filter(Operator.username == username).first()
        if not op or op.password != password:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # log activity
        activity = OperatorActivity(
            operator_id=op.id,
            action="login",
            timestamp=datetime.now()
        )
        db.add(activity)
        db.commit()

        return {"login": True, "operator_id": op.id, "role": op.role}

    finally:
        db.close()


# -------------------------
# LIST OPERATORS
# -------------------------

def list_operators():
    db = SessionLocal()
    try:
        return db.query(Operator).all()
    finally:
        db.close()


# -------------------------
# CREATE OPERATOR
# -------------------------

def create_operator(username: str, password: str, role: str):
    db = SessionLocal()
    try:
        op = Operator(username=username, password=password, role=role)
        db.add(op)
        db.commit()
        db.refresh(op)
        return op
    finally:
        db.close()


# -------------------------
# UPDATE ROLE
# -------------------------

def update_operator_role(operator_id: int, role: str):
    db = SessionLocal()
    try:
        op = db.query(Operator).filter(Operator.id == operator_id).first()
        if not op:
            raise HTTPException(status_code=404, detail="Operator not found")

        op.role = role
        db.commit()
        return {"updated": True, "role": role}

    finally:
        db.close()


# -------------------------
# ACTIVITY LOG
# -------------------------

def get_activity_log():
    db = SessionLocal()
    try:
        return db.query(OperatorActivity).order_by(OperatorActivity.timestamp.desc()).all()
    finally:
        db.close()


# -------------------------
# SHIFT START
# -------------------------

def start_shift(operator_id: int):
    db = SessionLocal()
    try:
        shift = OperatorShift(
            operator_id=operator_id,
            start_time=datetime.now(),
            end_time=None
        )
        db.add(shift)

        # log activity
        activity = OperatorActivity(
            operator_id=operator_id,
            action="shift_start",
            timestamp=datetime.now()
        )
        db.add(activity)

        db.commit()
        return {"shift_started": True}

    finally:
        db.close()


# -------------------------
# SHIFT END
# -------------------------

def end_shift(operator_id: int):
    db = SessionLocal()
    try:
        shift = db.query(OperatorShift).filter(
            OperatorShift.operator_id == operator_id,
            OperatorShift.end_time == None
        ).first()

        if not shift:
            raise HTTPException(status_code=400, detail="No active shift")

        shift.end_time = datetime.now()

        # log activity
        activity = OperatorActivity(
            operator_id=operator_id,
            action="shift_end",
            timestamp=datetime.now()
        )
        db.add(activity)

        db.commit()
        return {"shift_ended": True}

    finally:
        db.close()
