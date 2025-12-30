from datetime import datetime
from app.schemas import BookingRead


class ParkingMyCarImporter:
    @staticmethod
    def parse_row(row: dict) -> BookingRead:
        return BookingRead(
            customer_name=row.get("full_name"),
            customer_email=row.get("email"),
            checkin=datetime.fromisoformat(row["check_in"]),
            checkout=datetime.fromisoformat(row["check_out"]),
            passenger_count=int(row.get("passengers", 1)),
            portal="parkingmycar",
            raw_data=row,
        )
