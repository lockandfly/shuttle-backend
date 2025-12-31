import pandas as pd
from datetime import datetime
from app.bookings.services.import_service import ImportService

# ---------------------------------------------------------
# MOCK DB SESSION
# ---------------------------------------------------------
class MockDB:
    def __init__(self):
        self.items = []

    def add(self, obj):
        self.items.append(obj)

    def commit(self):
        pass


# ---------------------------------------------------------
# TEST PARKINGMYCAR
# ---------------------------------------------------------
def test_parkingmycar():
    row = pd.Series({
        "Cliente": "Mario Rossi",
        "Dettagli Veicolo": "Fiat Panda - AB123CD",
        "Check-in": "2025-12-10 10:00",
        "Check-out": "2025-12-15 18:00",
        "Importo pagato online": "45.50 €",
        "Stato": "Approvata"
    })

    result = ImportService.parse_parkingmycar(row)

    assert result["customer_name"] == "Mario Rossi"
    assert result["license_plate"] == "AB123CD"
    assert result["price"] == 45.50


# ---------------------------------------------------------
# TEST PARKOS
# ---------------------------------------------------------
def test_parkos():
    row = pd.Series({
        "name": "Simona Mitkova",
        "email": "simo@example.com",
        "car_sign": "DG284KX",
        "arrival": "12/11/2025 02:30:00",
        "departure": "12/18/2025 19:30:00",
        "price": 4100,
        "parking": "Lock & Fly Malpensa"
    })

    result = ImportService.parse_parkos(row)

    assert result["customer_name"] == "Simona Mitkova"
    assert result["license_plate"] == "DG284KX"
    assert result["price"] == 41.00


# ---------------------------------------------------------
# TEST MYPARKING
# ---------------------------------------------------------
def test_myparking():
    row = pd.Series({
        "Nominativo": "Giovanni Bianchi",
        "Targa": "AB123CD",
        "Ingresso": "24/12/2025 11:00",
        "Uscita": "01/01/2026 18:30",
        "Pagato online": "130,00",
        "Area Sosta": "Coperto"
    })

    result = ImportService.parse_myparking(row)

    assert result["customer_name"] == "Giovanni Bianchi"
    assert result["price"] == 130.00


# ---------------------------------------------------------
# TEST LOCKANDFLY
# ---------------------------------------------------------
def test_lockandfly():
    row = pd.Series({
        "customer": "Paolo Neri",
        "email": "paolo@example.com",
        "plate": "GH012IJ",
        "arrival": "2025-12-10T10:00",
        "departure": "2025-12-15T18:00",
        "price": "40.00",
        "notes": "Interno"
    })

    result = ImportService.parse_lockandfly(row)

    assert result["customer_name"] == "Paolo Neri"
    assert result["license_plate"] == "GH012IJ"
    assert result["price"] == 40.00
