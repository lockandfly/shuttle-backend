import json
from datetime import datetime
from sqlalchemy.orm import Session

from app.bookings.models_orm import Booking
from app.portals.enums import Portal


class ParkingMyCarImporter:

    @staticmethod
    def import_booking(row: dict, db: Session):
        """
        Import di una singola prenotazione ParkingMyCar.
        """

        # -------------------------
        # 1) Normalizzazione targa
        # -------------------------
        plate = (
            row.get("Dettagli Veicolo")
            or row.get("Targa")
            or row.get("Tipologia Veicolo")
            or ""
        )

        try:
            plate = str(plate).strip().upper()
        except:
            plate = ""

        if plate in ["", "NAN", "NONE", "NULL"]:
            plate = None

        # -------------------------
        # 2) Estrazione campi base
        # -------------------------
        code = row.get("ID") or None
        customer_name = row.get("Cliente") or None
        customer_email = None  # ParkingMyCar non fornisce email

        phone = None
        customer_phone = None

        # -------------------------
        # 3) Date e orari (chiavi corrette)
        # -------------------------
        def parse_dt(value):
            if not value:
                return None

            value = str(value).strip()

            formats = [
                "%Y-%m-%d %H:%M",       # formato reale del tuo CSV
                "%Y-%m-%d %H:%M:%S",
                "%d/%m/%Y %H:%M",
                "%d/%m/%Y %H.%M",
                "%d-%m-%Y %H:%M",
            ]

            for fmt in formats:
                try:
                    return datetime.strptime(value, fmt)
                except:
                    pass

            try:
                return datetime.fromisoformat(value)
            except:
                return None

        arrival = parse_dt(row.get("Check-in"))
        departure = parse_dt(row.get("Check-out"))

        if arrival is None or departure is None:
            raise ValueError("Formato data non riconosciuto")

        arrival_time = arrival
        departure_time = departure

        # -------------------------
        # 4) Prezzi
        # -------------------------
        def parse_price(value):
            if value is None:
                return None
            try:
                return float(str(value).replace("€", "").replace(",", ".").strip())
            except:
                return None

        base_price = parse_price(row.get("Tariffario"))
        final_price = parse_price(row.get("Importo pagato online"))

        # -------------------------
        # 5) Altri campi
        # -------------------------
        passengers = 1
        days = None
        passenger_count = 1
        notes = None
        parking_area = "standard"

        # -------------------------
        # 6) Raw data
        # -------------------------
        try:
            raw_data = json.dumps(row, ensure_ascii=False)
        except:
            raw_data = "{}"

        # -------------------------
        # 7) Creazione booking
        # -------------------------
        booking = Booking(
            portal=Portal.parkingmycar,
            code=code,
            customer_name=customer_name,
            customer_email=customer_email,
            phone=phone,
            customer_phone=customer_phone,
            license_plate=plate,
            arrival=arrival,
            departure=departure,
            arrival_time=arrival_time,
            departure_time=departure_time,
            price=final_price,
            payment_complete=None,
            external_id=None,
            online_payment=None,
            payment_option=None,
            cancel_date=None,
            cancel_reason=None,
            passengers=passengers,
            days=days,
            passenger_count=passenger_count,
            notes=notes,
            parking_area=parking_area,
            base_price=base_price,
            final_price=final_price,
            pricing_breakdown="null",
            pricing_reasoning="dynamic pricing not applied",
            status="active",
            raw_data=raw_data,
        )

        db.add(booking)
        db.commit()
        db.refresh(booking)

        return booking
