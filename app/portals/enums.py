from enum import Enum

class Portal(str, Enum):
    parkos = "parkos"
    myparking = "myparking"
    parkingmycar = "parkingmycar"
    direct = "direct"

    @property
    def description(self) -> str:
        descriptions = {
            "parkos": "Parkos external booking portal",
            "myparking": "MyParking external booking portal",
            "parkingmycar": "ParkingMyCar external booking portal",
            "direct": "Direct internal bookings",
        }
        return descriptions[self.value]
