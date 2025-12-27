import csv
import io
from datetime import datetime
from typing import List
import openpyxl

from app.bookings.models import BookingRead


class ParkingMyCarImporter:
    COLUMN_MAP = {
        "reservation_id": ["id"],
        "customer_name": ["cliente"],
        "checkin": ["check-in", "check in"],
        "checkout": ["check-out", "check out"],
    }

    DATE_FORMATS = [
        "%Y-%m-%d %H:%M",
        "%d/%m/%Y %H:%M",
    ]

    def parse(self, file_obj, filename: str) -> List[BookingRead]:
        filename = filename.lower()

        if filename.endswith(".csv"):
            rows = self._parse_csv(file_obj)
        elif filename.endswith(".xlsx"):
            rows = self._parse_xlsx(file_obj)
        else:
            raise ValueError("Formato file non supportato. Usa CSV o XLSX.")

        return self._convert_rows(rows)

    def _parse_csv(self, file_obj):
        content = file_obj.read().decode("utf-8", errors="ignore")
        content = content.replace("\ufeff", "")
        reader = csv.DictReader(io.StringIO(content))
        return list(reader)

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
                if value is None:
                    raise KeyError(f"{key}")
                extracted[key] = value

            checkin = self._parse_date(extracted["checkin"])
            checkout = self._parse_date(extracted["checkout"])

            booking = BookingRead(
                id=f"pmc-{extracted['reservation_id']}",
                portal="parkingmycar",
                portal_reservation_id=str(extracted["reservation_id"]),
                customer_name=str(extracted["customer_name"]),
                checkin=checkin,
                checkout=checkout,
                updated_at=datetime.utcnow(),
            )

            bookings.append(booking)

        return bookings

    def _parse_date(self, value):
        value = str(value).strip()
        for fmt in self.DATE_FORMATS:
            try:
                return datetime.strptime(value, fmt)
            except:
                pass
        raise ValueError(f"Formato data non riconosciuto: {value}")
