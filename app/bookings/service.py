from typing import Iterable, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.bookings.models import Booking, BookingCreate


def upsert_bookings(db: Session, items: Iterable[BookingCreate]) -> List[Booking]:
    """
    Inserisce prenotazioni evitando duplicati per (portal, portal_reservation_id).
    Se esiste già, per ora salta (no update).
    """
    created: List[Booking] = []

    for item in items:
        # Controllo se esiste già
        stmt = select(Booking).where(
            Booking.portal == item.portal,
            Booking.portal_reservation_id == item.portal_reservation_id,
        )
        existing = db.execute(stmt).scalar_one_or_none()
        if existing:
            continue

        booking = Booking(
            portal=item.portal,
            portal_reservation_id=item.portal_reservation_id,
            customer_name=item.customer_name,
            email=item.email,
            phone=item.phone,
            checkin=item.checkin,
            checkout=item.checkout,
            car_plate=item.car_plate,
            price=item.price,
        )

        db.add(booking)
        created.append(booking)

    db.commit()

    for b in created:
        db.refresh(b)

    return created
