from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import shutil
import os
from sqlalchemy.orm import Session

from app.database import get_db
from app.bookings.services.import_service import ImportService

router = APIRouter(
    prefix="/import",
    tags=["Import"]
)


@router.post("/")
async def import_bookings(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Import automatico delle prenotazioni.
    - Salva temporaneamente il file
    - Passa il percorso a ImportService
    - Ritorna il risultato dell'import
    """

    # 1) Salvataggio temporaneo del file
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)

    file_path = os.path.join(temp_dir, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore salvataggio file: {str(e)}")

    # 2) Import automatico (auto-detection del portale)
    try:
        result = ImportService.import_file(file_path, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        # 3) Pulizia file temporaneo
        if os.path.exists(file_path):
            os.remove(file_path)

    return result
