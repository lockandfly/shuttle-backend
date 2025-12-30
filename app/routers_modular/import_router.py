from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.import_service import import_csv, import_rows, list_last_imported

router = APIRouter(prefix="/import", tags=["Import"])


# -------------------------
# IMPORT CSV
# -------------------------

@router.post("/csv/{portal}")
async def import_csv_endpoint(portal: str, file: UploadFile = File(...)):
    return import_csv(portal, file)


# -------------------------
# IMPORT JSON ROWS
# -------------------------

@router.post("/rows/{portal}")
async def import_rows_endpoint(portal: str, rows: list[dict]):
    return import_rows(portal, rows)


# -------------------------
# LIST LAST IMPORTED
# -------------------------

@router.get("/last")
async def list_last():
    return list_last_imported()
