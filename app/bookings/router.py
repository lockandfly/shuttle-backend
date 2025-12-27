from fastapi import APIRouter, UploadFile, HTTPException, Query
from typing import List, Literal

from app.bookings.models import BookingRead
from app.bookings.importer.parkingmycar import ParkingMyCarImporter
from app.bookings.importer.myparking import MyParkingImporter
from app.bookings.importer.parkos import ParkosImporter


router = APIRouter(prefix="/import", tags=["Import Bookings"])

IMPORTERS = {
    "parkingmycar": ParkingMyCarImporter(),
    "myparking": MyParkingImporter(),
    "parkos": ParkosImporter(),
}


@router.post("", response_model=List[BookingRead])
async def import_bookings(
    portal: Literal["parkingmycar", "myparking", "parkos"] = Query(
        description="Seleziona il portale da cui importare"
    ),
    file: UploadFile = None
):
    if portal not in IMPORTERS:
        raise HTTPException(status_code=400, detail="Portale non supportato")

    importer = IMPORTERS[portal]

    try:
        bookings = importer.parse(file.file, file.filename)
        return bookings

    except KeyError as e:
        raise HTTPException(status_code=422, detail=f"Colonna mancante nel file: {e}")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore parsing file: {e}")
