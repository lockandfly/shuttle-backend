from sqlalchemy.orm import Session
from app.bookings.models_orm import Booking
from app.bookings.portal_enum import Portal
from app.utils.normalization import normalize_license_plate, normalize_name
from app.utils.service_type import detect_service_type
from app.utils.date_parser import parse_date
import re


class ParkingMyCarImporter:

    @staticmethod
    def extract_license_plate(vehicle_details: str) -> str:
        """
        Estrae la targa da stringhe tipo:
        "Suzuki Swift - GV138MZ"
        "Fiat Panda - AB123CD"
        """
        if not vehicle_details:
            return None

        # Cerca pattern targa italiana
        match = re.search(r"[A-Z]{2}\d{3}[A-Z]{2}", vehicle_details.upper())
        if match:
            return match.group(0)

        return None

    @staticmethod
    def import_booking(row: dict, db: Session) -> Booking:
        # -----------------------------
        # NOME CLIENTE
        # -----------------------------
        customer_name = normalize_name(row.get("Cliente"))

        # -----------------------------
        # EMAIL (ParkingMyCar non la fornisce sempre)
        # -----------------------------
        customer_email = row.get("Email") or None

        # -----------------------------
        # TELEFONO (non presente nel file → None)
        # -----------------------------
        customer_phone = None

        # -----------------------------
        # TARGA (estratta da "Dettagli Veicolo")
        # -----------------------------
        license_plate = ParkingMyCarImporter.extract_license_plate(
            row.get("Dettagli Veicolo")
        )
        license_plate = normalize_license_plate(license_plate)

        # -----------------------------
        # DATE
        # -----------------------------
        arrival = parse_date(row.get("Check-in"))
        departure = parse_date(row.get("Check-out"))

        # -----------------------------
        # PASSEGGERI (ParkingMyCar non lo fornisce → default 1)
        # -----------------------------
        passenger_count = 1

        # -----------------------------
        # PREZZI
        # -----------------------------
        base_price_raw = row.get("Importo pagato online") or row.get("Tariffario")

        try:
            base_price = float(str(base_price_raw).replace("€", "").replace(",", "."))
        except:
            base_price = 0.0

        final_price = base_price

        pricing_breakdown = None
        pricing_reasoning = "dynamic pricing not applied"

        # -----------------------------
        # TIPO SERVIZIO
        # -----------------------------
        service_description = row.get("Tariffario") or ""
        parking_area = detect_service_type(service_description)

        # -----------------------------
        # STATO
        # -----------------------------
        stato_raw = str(row.get("Stato") or "").lower()

        if "approv" in stato_raw:
            status = "active"
        elif "annull" in stato_raw or "cancel" in stato_raw:
            status = "cancelled"
        else:
            status = "active"

        # -----------------------------
        # CREAZIONE BOOKING
        # -----------------------------
        booking = Booking(
            portal=Portal.parkingmycar.value,
            code=row.get("ID"),

            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,

            license_plate=license_plate,

            arrival=arrival,
            departure=departure,
            arrival_time=arrival,
            departure_time=departure,

            passenger_count=passenger_count,
            passengers=passenger_count,

            base_price=base_price,
            final_price=final_price,
            pricing_breakdown=pricing_breakdown,
            pricing_reasoning=pricing_reasoning,

            parking_area=parking_area,
            status=status,

            raw_data=row,
        )

        db.add(booking)
        db.commit()
        db.refresh(booking)

        return booking
