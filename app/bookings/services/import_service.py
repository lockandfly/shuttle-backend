import pandas as pd
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.bookings.importer.parkos_importer import ParkosImporter
from app.bookings.importer.myparking_importer import MyParkingImporter
from app.bookings.importer.parkingmycar_importer import ParkingMyCarImporter
from app.bookings.portal_enum import Portal


class ImportService:

    @staticmethod
    def import_file(file_path: str, portal: str, db: Session):
        # -----------------------------
        # LETTURA FILE EXCEL
        # -----------------------------
        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Errore lettura file: {str(e)}")

        if df.empty:
            raise HTTPException(status_code=400, detail="Il file è vuoto")

        imported = []
        errors = []

        # -----------------------------
        # PROCESSA OGNI RIGA
        # -----------------------------
        for index, row in df.iterrows():
            try:
                row_dict = row.to_dict()

                # PARKOS
                if portal == Portal.parkos.value:
                    booking = ParkosImporter.import_booking(row_dict, db)

                # MYPARKING
                elif portal == Portal.myparking.value:
                    booking = MyParkingImporter.import_booking(row_dict, db)

                # PARKINGMYCAR
                elif portal == Portal.parkingmycar.value:
                    booking = ParkingMyCarImporter.import_booking(row_dict, db)

                else:
                    raise HTTPException(status_code=400, detail=f"Portale non supportato: {portal}")

                imported.append(booking)

            except Exception as e:
                errors.append({
                    "row": index + 2,  # Excel: header = riga 1, prima riga dati = riga 2
                    "error": str(e)
                })

        # -----------------------------
        # RISULTATO FINALE
        # -----------------------------
        return {
            "imported_count": len(imported),
            "error_count": len(errors),
            "errors": errors
        }
