from app.bookings.importer.myparking import MyParkingImporter
from app.bookings.importer.parkos import ParkosImporter
from app.bookings.importer.parkingmycar import ParkingMyCarImporter


class ImporterFactory:
    """
    Factory che restituisce l'importer corretto in base al nome del portale.
    """

    @staticmethod
    def get_importer(portal: str):
        portal = portal.lower().strip()

        if portal == "myparking":
            return MyParkingImporter

        if portal == "parkos":
            return ParkosImporter

        if portal == "parkingmycar":
            return ParkingMyCarImporter

        return None
