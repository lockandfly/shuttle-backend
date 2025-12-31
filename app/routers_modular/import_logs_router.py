from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/import", tags=["Import Logs"])

# In memoria (per ora)
IMPORT_LOGS = []

def log_import(portal, count):
    IMPORT_LOGS.append({
        "portal": portal,
        "count": count,
        "timestamp": datetime.now().isoformat()
    })

@router.get("/logs")
def get_import_logs():
    return IMPORT_LOGS
