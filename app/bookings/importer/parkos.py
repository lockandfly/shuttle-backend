from datetime import datetime
from typing import List
import csv
import io

from app.bookings.models import BookingRead


class ParkosImporter:
    COLUMN_MAP = {
        "reservation_id": ["reservation id", "id", "booking id"],
        "customer_name": ["name", "customer", "customer name"],
        "checkin": ["check-in", "arrival", "arrival time"],
        "checkout": ["check-out", "departure", "departure time"],
    }

    DATE_FORMATS = [
        "%Y-%m-%d %H:%M",
        "%d/%m/%Y %H:%M",
    ]

    def parse(self, file_obj, filename: str) -> List[BookingRead]:
        content = file_obj.read().decode("utf-8", errors="ignore")
        reader = csv.DictReader(io.StringIO(content))
        rows = list(reader)
        return self._convert_rows(rows)

    def _normalize(self, value):
        if value is None:
            return ""
        return str(value).strip().lower()

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
                id=f"parkos-{extracted['reservation_id']}",
                portal="parkos",
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
