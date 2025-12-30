from datetime import datetime
from app.schemas import BookingRead


class MyParkingImporter:
    @staticmethod
    def parse_row(row: dict) -> BookingRead:
        return BookingRead(
            customer_name=row.get("customer_name"),
            customer_email=row.get("customer_email"),
            checkin=datetime.fromisoformat(row["checkin"]),
            checkout=datetime.fromisoformat(row["checkout"]),
            passenger_count=int(row.get("passenger_count", 1)),
            portal="myparking",
            raw_data=row,
        )
