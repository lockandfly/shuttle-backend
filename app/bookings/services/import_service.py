import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime
from app.bookings.models import Booking
from app.bookings.services.import_validation import ImportValidator
from app.routers_modular.import_logs_router import log_import

class ImportService:

    @staticmethod
    def import_file(file_path: str, portal: str, db: Session):
        # 1. Caricamento file
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        # 2. Validazione base
        ImportValidator.require_non_empty(df, portal)

        # 3. Parser map
        parser_map = {
            "parkos": ImportService.parse_parkos,
            "myparking": ImportService.parse_myparking,
            "parkingmycar": ImportService.parse_parkingmycar,
            "lockandfly": ImportService.parse_lockandfly,
        }

        if portal not in parser_map:
            raise ValueError(f"Portale non supportato: {portal}")

        parser = parser_map[portal]

        # 4. Parsing righe
        bookings = []
        for _, row in df.iterrows():
            booking_data = parser(row)
            booking = Booking(**booking_data)
            db.add(booking)
            bookings.append(booking)

        db.commit()

        # 5. Logging import
        log_import(portal, len(bookings))

        return bookings

    # ---------------------------------------------------------
    # PARSER SPECIFICI PER OGNI PORTALE
    # ---------------------------------------------------------

    @staticmethod
    def parse_parkingmycar(row):
        dettagli = row.get("Dettagli Veicolo", "")
        targa = None
        if "-" in dettagli:
            targa = dettagli.split("-")[-1].strip()

        prezzo_str = row.get("Importo pagato online", "0").replace("€", "").replace(",", ".").strip()
        prezzo = float(prezzo_str)

        return {
            "portal": "parkingmycar",
            "customer_name": row["Cliente"],
            "customer_email": None,
            "license_plate": targa,
            "arrival": datetime.strptime(row["Check-in"], "%Y-%m-%d %H:%M"),
            "departure": datetime.strptime(row["Check-out"], "%Y-%m-%d %H:%M"),
            "price": prezzo,
            "notes": row.get("Stato"),
        }

    @staticmethod
    def parse_parkos(row):
        price_raw = row.get("price", 0)
        try:
            price = float(price_raw) / 100
        except:
            price = 0.0

        arrival = datetime.strptime(row["arrival"], "%m/%d/%Y %H:%M:%S")
        departure = datetime.strptime(row["departure"], "%m/%d/%Y %H:%M:%S")

        return {
            "portal": "parkos",
            "customer_name": row["name"],
            "customer_email": row.get("email"),
            "license_plate": row.get("car_sign"),
            "arrival": arrival,
            "departure": departure,
            "price": price,
            "notes": row.get("parking"),
        }

    @staticmethod
    def parse_myparking(row):
        prezzo_str = str(row.get("Pagato online", "0")).replace(",", ".")
        prezzo = float(prezzo_str)

        return {
            "portal": "myparking",
            "customer_name": row["Nominativo"],
            "customer_email": None,
            "license_plate": row.get("Targa"),
            "arrival": datetime.strptime(row["Ingresso"], "%d/%m/%Y %H:%M"),
            "departure": datetime.strptime(row["Uscita"], "%d/%m/%Y %H:%M"),
            "price": prezzo,
            "notes": row.get("Area Sosta"),
        }

    @staticmethod
    def parse_lockandfly(row):
        return {
            "portal": "lockandfly",
            "customer_name": row["customer"],
            "customer_email": row.get("email"),
            "license_plate": row.get("plate"),
            "arrival": datetime.fromisoformat(row["arrival"]),
            "departure": datetime.fromisoformat(row["departure"]),
            "price": float(row["price"]),
            "notes": row.get("notes"),
        }
