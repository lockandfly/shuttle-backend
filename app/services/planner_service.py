from datetime import datetime
from app.database import SessionLocal
from app.planner.models_orm import Plan, PlanItem


def create_plan(name: str):
    db = SessionLocal()
    try:
        plan = Plan(name=name)
        db.add(plan)
        db.commit()
        db.refresh(plan)
        return plan
    finally:
        db.close()


def add_plan_item(plan_id: int, description: str):
    db = SessionLocal()
    try:
        item = PlanItem(plan_id=plan_id, description=description)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    finally:
        db.close()


def get_plan(plan_id: int):
    db = SessionLocal()
    try:
        return db.query(Plan).filter(Plan.id == plan_id).first()
    finally:
        db.close()


def list_plans():
    db = SessionLocal()
    try:
        return db.query(Plan).order_by(Plan.created_at.desc()).all()
    finally:
        db.close()
