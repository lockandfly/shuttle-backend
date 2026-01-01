import pandas as pd
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.bookings.importer.parkos_importer import ParkosImporter
from app.bookings.importer.myparking_importer import MyParkingImporter
from app.bookings.importer.parkingmycar_importer import ParkingMyCarImporter
from app.bookings.services.import_detection import ImportDetectionService
from app.portals.enums import Portal


class ImportService:

    @staticmethod
    def import_file(file_path: str, db: Session):
        """
        Import automatico:
        - rileva il portale dal file
        - usa l'importer corretto
        - gestisce errori riga per riga
        """
        # 1) Riconoscimento automatico del portale
        portal = ImportDetectionService.detect_portal_from_file(file_path)

        # 2) Lettura file (CSV o XLSX)
        try:
            if file_path.lower().endswith(".csv"):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Errore lettura file: {str(e)}")

        if df.empty:
            raise HTTPException(status_code=400, detail="Il file è vuoto")

        imported = []
        errors = []

        # 3) Elaborazione riga per riga
        for index, row in df.iterrows():
            try:
                row_dict = row.to_dict()

                if portal == Portal.parkos:
                    booking = ParkosImporter.import_booking(row_dict, db)

                elif portal == Portal.myparking:
                    booking = MyParkingImporter.import_booking(row_dict, db)

                elif portal == Portal.parkingmycar:
                    booking = ParkingMyCarImporter.import_booking(row_dict, db)

                else:
                    raise HTTPException(status_code=400, detail=f"Portale non supportato: {portal}")

                imported.append(booking)

            except Exception as e:
                errors.append({
                    "row": index + 2,
                    "error": str(e)
                })

        # 4) Risultato finale
        return {
            "portal_detected": portal.value,
            "imported_count": len(imported),
            "error_count": len(errors),
            "errors": errors
        }
