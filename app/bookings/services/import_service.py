import pandas as pd
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.bookings.importer.parkos_importer import ParkosImporter
from app.bookings.importer.myparking_importer import MyParkingImporter
from app.bookings.importer.parkingmycar_importer import ParkingMyCarImporter
from app.portals.enums import Portal


class ImportService:

    @staticmethod
    def import_file(file_path: str, portal: str, db: Session):
        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Errore lettura file: {str(e)}")

        if df.empty:
            raise HTTPException(status_code=400, detail="Il file è vuoto")

        imported = []
        errors = []

        for index, row in df.iterrows():
            try:
                row_dict = row.to_dict()

                if portal == Portal.parkos.value:
                    booking = ParkosImporter.import_booking(row_dict, db)

                elif portal == Portal.myparking.value:
                    booking = MyParkingImporter.import_booking(row_dict, db)

                elif portal == Portal.parkingmycar.value:
                    booking = ParkingMyCarImporter.import_booking(row_dict, db)

                else:
                    raise HTTPException(status_code=400, detail=f"Portale non supportato: {portal}")

                imported.append(booking)

            except Exception as e:
                errors.append({
                    "row": index + 2,
                    "error": str(e)
                })

        return {
            "imported_count": len(imported),
            "error_count": len(errors),
            "errors": errors
        }
