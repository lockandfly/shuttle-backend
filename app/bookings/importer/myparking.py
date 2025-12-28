import openpyxl
from datetime import datetime
from typing import List

from app.bookings.models import BookingRead


class MyParkingImporter:
    """
    Importer per MyParking.
    Supporta solo file XLSX.
    """

    COLUMN_MAP = {
        "reservation_id": ["codice prenotazione"],
        "customer_name": ["nominativo"],
        "checkin": ["ingresso"],
        "checkout": ["uscita"],
        "car_plate": ["targa"],
        "amount": ["da pagare"],
        "status": ["stato"],
        "parking_area": ["area sosta"],
        "customer_email": ["cliente"],  # opzionale
    }

    DATE_FORMATS = [
        "%d/%m/%Y %H:%M",
        "%Y-%m-%d %H:%M",
        "%d/%m/%Y",
        "%Y-%m-%d",
    ]

    def parse(self, file_obj, filename: str) -> List[BookingRead]:
        filename = filename.lower()

        if not filename.endswith(".xlsx"):
            raise ValueError("MyParking supporta solo file XLSX.")

        rows = self._parse_xlsx(file_obj)
        return self._convert_rows(rows)

    def _parse_xlsx(self, file_obj):
        wb = openpyxl.load_workbook(file_obj, data_only=True)
        ws = wb.active
        rows = list(ws.values)
        headers = [self._normalize(h) for h in rows[0]]
        parsed = []
        for row in rows[1:]:
            parsed.append({headers[i]: row[i] for i in range(len(headers))})
        return parsed

    def _normalize(self, value):
        if value is None:
            return ""
        return (
            str(value)
            .strip()
            .lower()
            .replace("\ufeff", "")
        )

    def _convert_rows(self, rows):
        bookings = []

        for row in rows:
            normalized = {self._normalize(k): v for k, v in row.items()}

            extracted = {}
            for key, variants in self.COLUMN_MAP.items():
                value = None
                for v in variants:
                    if v in normalized:
                        value = normalized[v]
                        break
                extracted[key] = value  # opzionali ammessi

            checkin = self._parse_date(extracted["checkin"])
            checkout = self._parse_date(extracted["checkout"])

            booking = BookingRead(
                id=f"myparking-{extracted['reservation_id']}",
                portal="myparking",
                portal_reservation_id=str(extracted["reservation_id"]),
                customer_name=str(extracted["customer_name"]),
                checkin=checkin,
                checkout=checkout,
                updated_at=datetime.utcnow(),
                # campi extra
                car_plate=extracted.get("car_plate"),
                customer_email=extracted.get("customer_email"),
                amount=extracted.get("amount"),
                status=extracted.get("status"),
                parking_area=extracted.get("parking_area"),
            )

            bookings.append(booking)

        return bookings

    def _parse_date(self, value):
        value = str(value).strip()

        for fmt in self.DATE_FORMATS:
            try:
                return datetime.strptime(value, fmt)
            except Exception:
                pass

        raise ValueError(f"Formato data non riconosciuto: {value}")
