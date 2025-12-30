from datetime import datetime
from app.schemas import BookingRead


class ParkosImporter:
    @staticmethod
    def parse_row(row: dict) -> BookingRead:
        return BookingRead(
            customer_name=row.get("name"),
            customer_email=row.get("email"),
            checkin=datetime.fromisoformat(row["arrival"]),
            checkout=datetime.fromisoformat(row["departure"]),
            passenger_count=int(row.get("pax", 1)),
            portal="parkos",
            raw_data=row,
        )
