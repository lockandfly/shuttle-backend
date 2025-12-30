from fastapi import APIRouter
from app.services.planner_service import (
    create_plan,
    add_plan_item,
    get_plan,
    list_plans,
)

router = APIRouter(prefix="/planner", tags=["Planner"])


@router.post("/create")
def create_new_plan(name: str):
    return create_plan(name)


@router.post("/add_item")
def add_item(plan_id: int, description: str):
    return add_plan_item(plan_id, description)


@router.get("/get")
def get_single_plan(plan_id: int):
    return get_plan(plan_id)


@router.get("/list")
def get_all_plans():
    return list_plans()
