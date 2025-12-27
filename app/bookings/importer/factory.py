from app.bookings.importer.parkingmycar import ParkingMyCarImporter
from app.bookings.importer.parkos import ParkosImporter
from app.bookings.importer.myparking import MyParkingImporter
from app.bookings.importer.base import BaseImporter

def get_importer(portal: str) -> BaseImporter:
    key = portal.strip().lower()

    if key == "parkingmycar":
        return ParkingMyCarImporter()
    if key == "parkos":
        return ParkosImporter()
    if key == "myparking":
        return MyParkingImporter()

    raise ValueError(f"Unsupported portal: {portal}")
