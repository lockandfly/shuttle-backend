from fastapi import APIRouter
from app.services.optimizer_service import (
    compute_time_slots,
    compute_assignments,
    compute_forecast,
    compute_scenario,
    run_full_optimizer,
    optimizer_debug_info
)

router = APIRouter(prefix="/optimizer", tags=["Optimizer"])


@router.get("/slots")
def optimizer_slots():
    return compute_time_slots()


@router.get("/assignments")
def optimizer_assignments():
    return compute_assignments()


@router.get("/forecast")
def optimizer_forecast():
    return compute_forecast()


@router.get("/scenario")
def optimizer_scenario(increase_percent: int = 10):
    return compute_scenario(increase_percent)


@router.post("/run")
def optimizer_run():
    return run_full_optimizer()


@router.get("/debug")
def optimizer_debug():
    return optimizer_debug_info()
