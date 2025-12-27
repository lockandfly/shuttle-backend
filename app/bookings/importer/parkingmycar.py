import csv
import io
from datetime import datetime
from typing import List
import openpyxl

from app.bookings.models import BookingRead


class ParkingMyCarImporter:
    """
    Importer unificato per ParkingMyCar.
    Supporta CSV e XLSX.
    Normalizza intestazioni e valori.
    """

    # Mappa colonne → possibili varianti nei file reali
    COLUMN_MAP = {
        "reservation_id": ["id", "codice", "prenotazione", "reservation id"],
        "checkin": ["check-in", "check in", "arrivo"],
        "checkout": ["check-out", "check out", "partenza"],
        "customer_name": ["cliente", "nome cliente"],
        "customer_email": ["email", "mail"],
    }

    # Formati data più comuni nei file ParkingMyCar
    DATE_FORMATS = [
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
    ]

    def parse(self, file_obj, filename: str) -> List[BookingRead]:
        """
        Auto-detect CSV o XLSX e avvia il parsing.
        """
        filename = filename.lower()

        if filename.endswith(".csv"):
            rows = self._parse_csv(file_obj)
        elif filename.endswith(".xlsx"):
            rows = self._parse_xlsx(file_obj)
        else:
            raise ValueError("Formato file non supportato. Usa CSV o XLSX.")

        return self._convert_rows(rows)

    # ------------------------------------------------------------
    # PARSING CSV
    # ------------------------------------------------------------
    def _parse_csv(self, file_obj):
        content = file_obj.read().decode("utf-8", errors="ignore")
        content = content.replace("\ufeff", "")  # Rimuove BOM

        reader = csv.DictReader(io.StringIO(content))
        return list(reader)

    # ------------------------------------------------------------
    # PARSING XLSX
    # ------------------------------------------------------------
    def _parse_xlsx(self, file_obj):
        wb = openpyxl.load_workbook(file_obj, data_only=True)
        ws = wb.active

        rows = list(ws.values)
        headers = [self._normalize(h) for h in rows[0]]
        data_rows = rows[1:]

        parsed = []
        for row in data_rows:
            parsed.append({headers[i]: row[i] for i in range(len(headers))})

        return parsed

    # ------------------------------------------------------------
    # NORMALIZZAZIONE
    # ------------------------------------------------------------
    def _normalize(self, value):
        if value is None:
            return ""
        return (
            str(value)
            .strip()
            .lower()
            .replace("\xa0", " ")
            .replace("\n", " ")
            .replace("\t", " ")
            .replace("\ufeff", "")  # Rimuove BOM
        )

    # ------------------------------------------------------------
    # CONVERSIONE RIGHE → BookingRead
    # ------------------------------------------------------------
    def _convert_rows(self, rows):
        bookings = []

        for row in rows:
            normalized = {self._normalize(k): v for k, v in row.items()}

            # Estrai colonne richieste
            extracted = {}
            for key, variants in self.COLUMN_MAP.items():
                value = None
                for v in variants:
                    if v in normalized:
                        value = normalized[v]
                        break
                if value is None