from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.optimizer.service import run_optimizer
from app.optimizer.schemas import OptimizerRequest, OptimizerResponse

router = APIRouter(
    prefix="",
    tags=["Optimizer"]
)

@router.post("/run", response_model=OptimizerResponse)
def run_optimizer_endpoint(payload: OptimizerRequest, db: Session = Depends(get_db)):
    """
    Executes the operational optimizer, including:
    - shuttle load balancing
    - parking spot distribution
    - resource allocation
    - operational efficiency scoring
    """
    return run_optimizer(db, payload)
