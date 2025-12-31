from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
import shutil
import os

from app.database import get_db
from app.bookings.services.import_service import ImportService
from app.bookings.schemas_portal import Portal

router = APIRouter(prefix="/import", tags=["Import"])

@router.post("/")
async def import_bookings(
    portal: Portal = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Importa un file CSV/XLSX per un portale specifico.
    """

    # -----------------------------
    # 1. Salvataggio temporaneo file
    # -----------------------------
    temp_path = f"/tmp/{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # -----------------------------
    # 2. Importazione tramite service
    # -----------------------------
    try:
        bookings = ImportService.import_file(
            file_path=temp_path,
            portal=portal.value,
            db=db
        )
    finally:
        # Pulizia file temporaneo
        if os.path.exists(temp_path):
            os.remove(temp_path)

    # -----------------------------
    # 3. Risposta
    # -----------------------------
    return {
        "imported": len(bookings),
        "portal": portal.value,
        "bookings": [b.id for b in bookings]
    }
