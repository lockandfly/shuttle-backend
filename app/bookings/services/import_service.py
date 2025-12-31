import csv
import pandas as pd
from sqlalchemy.orm import Session

from app.bookings.importer.parkos_importer import ParkosImporter
from app.bookings.importer.myparking_importer import MyParkingImporter
from app.bookings.importer.parkingmycar_importer import ParkingMyCarImporter


class ImportService:

    IMPORTERS = {
        "parkos": ParkosImporter,
        "myparking": MyParkingImporter,
        "parkingmycar": ParkingMyCarImporter,
    }

    @staticmethod
    def load_file(file_path: str) -> list[dict]:
        """
        Carica un file CSV o XLSX e restituisce una lista di dict.
        """
        if file_path.endswith(".csv"):
            with open(file_path, encoding="utf-8") as f:
                return list(csv.DictReader(f))

        if file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
            return df.to_dict(orient="records")

        raise ValueError("Formato file non supportato. Usa CSV o XLSX.")

    @classmethod
    def import_file(cls, file_path: str, portal: str, db: Session) -> list:
        """
        Importa un file intero per un portale specifico.
        """
        portal = portal.lower()

        importer_class = cls.IMPORTERS.get(portal)
        if not importer_class:
            raise ValueError(f"Portale non riconosciuto: {portal}")

        rows = cls.load_file(file_path)

        imported_bookings = []

        for row in rows:
            try:
                booking = importer_class.import_booking(row, db)
                imported_bookings.append(booking)
            except Exception as e:
                print(f"Errore importando riga: {row}")
                print(f"Dettaglio errore: {e}")

        return imported_bookings

    @classmethod
    def import_single_row(cls, portal: str, row: dict, db: Session):
        """
        Importa una singola riga per un portale specifico.
        """
        portal = portal.lower()

        importer_class = cls.IMPORTERS.get(portal)
        if not importer_class:
            raise ValueError(f"Portale non riconosciuto: {portal}")

        return importer_class.import_booking(row, db)
