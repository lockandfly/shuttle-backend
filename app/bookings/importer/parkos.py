import csv
import io
from datetime import datetime
from typing import List

from app.bookings.models import BookingRead


class ParkosImporter:
    """
    Importer per Parkos.
    Supporta solo file CSV.
    """

    COLUMN_MAP = {
        "reservation_id": ["code"],
        "customer_name": ["name"],
        "customer_email": ["email"],
        "customer_phone": ["phonenumber"],
        "car_model": ["car"],
        "car_plate": ["car_sign"],
        "checkin": ["arrival"],
        "checkout": ["departure"],
        "created_at": ["createdat"],
        "amount": ["price"],
        "status": ["paymentcomplete", "cancelreason"],
        "parking_area": ["parking"],
        "note": ["products"],
        "payment_method": ["onlinepayment", "paymentoption"],
        "cancel_reason": ["cancelreason"],
        "passenger_count": ["numberofpassengers"],
        "calendar_days": ["numberofcalendardays"],
    }

    DATE_FORMATS = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%d/%m/%Y %H:%M",
    ]

    def parse(self, file_obj, filename: str) -> List[BookingRead]:
        filename = filename.lower()

        if not filename.endswith(".csv"):
            raise ValueError("Parkos supporta solo file CSV.")

        rows = self._parse_csv(file_obj)
        return self._convert_rows(rows)

    def _parse_csv(self, file_obj):
        content = file_obj.read().decode("utf-8", errors="ignore")
        content = content.replace("\ufeff", "")
        reader = csv.DictReader(io.StringIO(content))
        return list(reader)

    def _normalize(self, value):
        if value is None:
            return ""
        return str(value).strip().lower()

    def _clean_phone(self, value):
        if not value:
            return None
        return (
            str(value)
            .replace("+39", "")
            .replace(" ", "")
            .replace("-", "")
            .strip()
        )

    def _convert_price(self, value):
        try:
            return str(round(float(value), 2))
        except Exception:
            return None

    def _convert_int(self, value):
        try:
            return int(value)
        except Exception:
            return None

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
                extracted[key] = value

            checkin = self._parse_date(extracted["checkin"])
            checkout = self._parse_date(extracted["checkout"])
            created_at = self._parse_date_optional(extracted.get("created_at"))

            # status intelligente
            status = None
            if extracted.get("cancel_reason"):
                status = "cancelled"
            elif extracted.get("status") == "sì":
                status = "paid"

            # metodo di pagamento
            payment_method = None
            if extracted.get("payment_method") == "sì":
                payment_method = "online"
            elif extracted.get("payment_method"):
                payment_method = extracted["payment_method"]

            booking = BookingRead(
                id=f"parkos-{extracted['reservation_id']}",
                portal="parkos",
                portal_reservation_id=str(extracted["reservation_id"]),
                customer_name=str(extracted["customer_name"]),
                customer_email=extracted.get("customer_email"),
                customer_phone=self._clean_phone(extracted.get("customer_phone")),
                car_model=extracted.get("car_model"),
                car_plate=extracted.get("car_plate"),
                checkin=checkin,
                checkout=checkout,
                created_at=created_at,
                updated_at=datetime.utcnow(),
                amount=self._convert_price(extracted.get("amount")),
                status=status,
                parking_area=extracted.get("parking_area"),
                note=extracted.get("note"),
                payment_method=payment_method,
                cancel_reason=extracted.get("cancel_reason"),
                passenger_count=self._convert_int(extracted.get("passenger_count")),
                calendar_days=self._convert_int(extracted.get("calendar_days")),
            )

            bookings.append(booking)

        return bookings

    def _parse_date(self, value):
        if not value:
            raise ValueError("Data mancante")

        value = str(value).strip()

        for fmt in self.DATE_FORMATS:
            try:
                return datetime.strptime(value, fmt)
            except Exception:
                pass

        raise ValueError(f"Formato data non riconosciuto: {value}")

    def _parse_date_optional(self, value):
        if not value:
            return None

        value = str(value).strip()

        for fmt in self.DATE_FORMATS:
            try:
                return datetime.strptime(value, fmt)
            except Exception:
                pass

        return None
