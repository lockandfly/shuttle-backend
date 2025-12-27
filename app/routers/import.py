from fastapi import APIRouter, UploadFile, HTTPException
from typing import List

from app.bookings.models import BookingRead

# Importer unificati
from app.bookings.importer.parkingmycar import ParkingMyCarImporter
from app.bookings.importer.myparking import MyParkingImporter


router = APIRouter(prefix="/import", tags=["Import Bookings"])


# Dispatcher dei portali
IMPORTERS = {
    "parkingmycar": ParkingMyCarImporter(),
    "myparking": MyParkingImporter(),
}


@router.post("", response_model=List[BookingRead])
async def import_bookings(portal: str, file: UploadFile):
    """
    Importa prenotazioni da vari portali.
    Supporta CSV e XLSX.
    Restituisce BookingRead simulati.
    """

    portal = portal.lower()

    # Verifica portale supportato
    if portal not in IMPORTERS:
        raise HTTPException(
            status_code=400,
            detail=f"Portale '{portal}' non supportato. Usa: {list(IMPORTERS.keys())}"
        )

    importer = IMPORTERS[portal]

    try:
        # Passiamo sia file.file che filename per auto-detect CSV/XLSX
        bookings = importer.parse(file.file, file.filename)
        return bookings

    except KeyError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Colonna mancante nel file: {str(e)}"
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Errore durante il parsing: {str(e)}"
        )
