from sqlalchemy.orm import Session
from app.parking.models_orm import ParkingSpot, SpotStatus


def get_current_occupancy(db: Session):
    """
    Calcola l'occupazione totale dei parcheggi.
    """

    total = db.query(ParkingSpot).count()
    occupied = (
        db.query(ParkingSpot)
        .filter(ParkingSpot.status == SpotStatus.OCCUPIED)
        .count()
    )
    free = total - occupied

    occupancy_rate = occupied / total if total > 0 else 0

    return {
        "total_spots": total,
        "occupied_spots": occupied,
        "free_spots": free,
        "occupancy_rate": round(occupancy_rate, 3),
    }
