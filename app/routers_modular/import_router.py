from fastapi import APIRouter, UploadFile, Depends, HTTPException, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.bookings.services.import_service import ImportService

router = APIRouter(
    prefix="/import",
    tags=["Import"],
)


@router.post("/", summary="Importa prenotazioni da file CSV/XLSX")
async def import_bookings(
    portal: str = Form(...),
    file: UploadFile = Form(...),
    db: Session = Depends(get_db)
):
    try:
        bookings = ImportService.import_file(
            db=db,
            file=file,
            portal=portal
        )

        return {
            "status": "success",
            "imported": len(bookings),
            "bookings": [b.id for b in bookings]
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
