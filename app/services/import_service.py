from datetime import datetime
from fastapi import UploadFile, HTTPException
import csv
import io

from app.database import SessionLocal
from app.schemas import BookingRead
from app.bookings.importer.factory import ImporterFactory
from app.bookings.models_orm import Booking


# -------------------------
# IMPORT CSV
# -------------------------

def import_csv(portal: str, file: UploadFile):
    """
    Importa un CSV da un portale specifico usando l'importer corretto.
    """
    importer = ImporterFactory.get_importer(portal)
    if not importer:
        raise HTTPException(status_code=400, detail=f"Unknown portal: {portal}")

    try:
        content = file.file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(content))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CSV file")

    db = SessionLocal()
    imported = []

    try:
        for row in reader:
            parsed: BookingRead = importer.parse_row(row)

            booking = Booking(
                customer_name=parsed.customer_name,
                customer_email=parsed.customer_email,
                checkin=parsed.checkin,
                checkout=parsed.checkout,
                passenger_count=parsed.passenger_count,
                portal=parsed.portal,
                parking_area=parsed.parking_area,
                raw_data=parsed.raw_data,
                created_at=datetime.now(),
            )

            db.add(booking)
            db.commit()
            db.refresh(booking)

            imported.append({
                "id": booking.id,
                "customer_name": booking.customer_name,
                "checkin": booking.checkin,
                "checkout": booking.checkout,
                "portal": booking.portal,
            })

        return {"imported": imported}

    finally:
        db.close()


# -------------------------
# IMPORT ROWS (JSON)
# -------------------------

def import_rows(portal: str, rows: list[dict]):
    """
    Importa una lista di dizionari JSON usando l'importer corretto.
    """
    importer = ImporterFactory.get_importer(portal)
    if not importer:
        raise HTTPException(status_code=400, detail=f"Unknown portal: {portal}")

    db = SessionLocal()
    imported = []

    try:
        for row in rows:
            parsed: BookingRead = importer.parse_row(row)

            booking = Booking(
                customer_name=parsed.customer_name,
                customer_email=parsed.customer_email,
                checkin=parsed.checkin,
                checkout=parsed.checkout,
                passenger_count=parsed.passenger_count,
                portal=parsed.portal,
                parking_area=parsed.parking_area,
                raw_data=parsed.raw_data,
                created_at=datetime.now(),
            )

            db.add(booking)
            db.commit()
            db.refresh(booking)

            imported.append({
                "id": booking.id,
                "customer_name": booking.customer_name,
                "checkin": booking.checkin,
                "checkout": booking.checkout,
                "portal": booking.portal,
            })

        return {"imported": imported}

    finally:
        db.close()


# -------------------------
# LIST LAST IMPORTED
# -------------------------

def list_last_imported(limit: int = 50):
    """
    Restituisce gli ultimi booking importati.
    """
    db = SessionLocal()
    try:
        bookings = (
            db.query(Booking)
            .order_by(Booking.created_at.desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "id": b.id,
                "customer_name": b.customer_name,
                "checkin": b.checkin,
                "checkout": b.checkout,
                "portal": b.portal,
            }
            for b in bookings
        ]

    finally:
        db.close()
