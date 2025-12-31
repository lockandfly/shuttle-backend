from fastapi import APIRouter
from app.portals.schemas import PortalResponse
from app.portals.enums import Portal

router = APIRouter(
    prefix="",
    tags=["Portals"]
)

@router.get("/", response_model=list[PortalResponse])
def list_portals():
    """
    Returns the list of supported portals:
    - parkos
    - myparking
    - parkingmycar
    - direct
    """
    return [
        PortalResponse(name=p.value, description=p.description)
        for p in Portal
    ]
