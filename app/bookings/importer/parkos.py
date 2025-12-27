import csv
from datetime import datetime
from typing import List

from app.bookings.importer.base import BaseImporter
from app.bookings.models import BookingCreate

class ParkosImporter(BaseImporter):

    def parse(self, file_path: str) -> List[BookingCreate]:
        bookings = []

        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                portal_reservation_id = row["code"]
                customer_name = row["name"]
                email = row.get("email") or None
                phone = row.get("phonenumber") or None

                checkin = datetime.strptime(row["arrival"], "%Y-%m-%d %H:%M:%S")
                checkout = datetime.strptime(row["departure"], "%Y-%m-%d %H:%M:%S")

                car_plate = row.get("car_sign") or None
                price = float(row["price"])

                bookings.append(
                    BookingCreate(
                        portal="Parkos",
                        portal_reservation_id=str(portal_reservation_id),
                        customer_name=customer_name,
                        email=email,
                        phone=phone,
                        checkin=checkin,
                        checkout=checkout,
                        car_plate=car_plate,
                        price=price,
                    )
                )

        return bookings
