from sqlalchemy.orm import Session
from app.bookings.models_orm import Booking
from app.bookings.portal_enum import Portal
from app.utils.normalization import normalize_license_plate, normalize_name
from app.utils.service_type import detect_service_type
from app.utils.date_parser import parse_date


class MyParkingImporter:

    @staticmethod
    def import_booking(row: dict, db: Session) -> Booking:
        customer_name = normalize_name(row.get("customer_name") or row.get("Nome") or row.get("nome_completo"))
        customer_email = row.get("customer_email") or row.get("email")
        license_plate = normalize_license_plate(row.get("license_plate") or row.get("Targa") or "")

        arrival = parse_date(row.get("checkin") or row.get("check_in"))
        departure = parse_date(row.get("checkout") or row.get("check_out"))

        try:
            passenger_count = int(row.get("passenger_count") or row.get("Passeggeri") or 1)
        except:
            passenger_count = 1

        base_price_raw = (
            row.get("importo_pagato_online")
            or row.get("paid_online")
            or row.get("price")
            or row.get("importo")
        )

        try:
            base_price = float(str(base_price_raw).replace("€", "").replace(",", "."))
        except:
            base_price = 0.0

        final_price = base_price
        pricing_breakdown = None
        pricing_reasoning = "dynamic pricing not applied (base listino non definito)"

        service_description = row.get("tariffario") or row.get("service") or ""
        parking_area = detect_service_type(service_description)

        status_raw = str(row.get("stato") or row.get("status") or "").lower()
        status = "cancelled" if "annull" in status_raw or "cancel" in status_raw else "active"

        booking = Booking(
            customer_name=customer_name,
            customer_email=customer_email,
            license_plate=license_plate,
            arrival_time=arrival,
            departure_time=departure,
            passenger_count=passenger_count,
            portal=Portal.myparking.value,
            parking_area=parking_area,
            base_price=base_price,
            final_price=final_price,
            pricing_breakdown=pricing_breakdown,
            pricing_reasoning=pricing_reasoning,
            status=status,
            raw_data=row,
        )

        db.add(booking)
        db.commit()
        db.refresh(booking)

        return booking
