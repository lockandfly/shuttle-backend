from fastapi import APIRouter
from app.services.portals_service import (
    list_portals,
    get_portal_config,
    update_portal_config,
    get_portal_health,
    get_portal_mapping,
    update_portal_mapping
)

router = APIRouter(prefix="/portals", tags=["Portals"])


@router.get("/list")
def portals_list():
    return list_portals()


@router.get("/config")
def portals_config(portal: str):
    return get_portal_config(portal)


@router.post("/update_config")
def portals_update_config(portal: str, key: str, value: str):
    return update_portal_config(portal, key, value)


@router.get("/health")
def portals_health(portal: str):
    return get_portal_health(portal)


@router.get("/mapping")
def portals_mapping(portal: str):
    return get_portal_mapping(portal)


@router.post("/mapping/update")
def portals_mapping_update(portal: str, field: str, mapped_to: str):
    return update_portal_mapping(portal, field, mapped_to)
