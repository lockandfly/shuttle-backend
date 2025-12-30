from datetime import datetime
from sqlalchemy.orm import Session

from app.parking.models_orm import ParkingArea, ParkingSpot, SpotStatus
from app.bookings.models_orm import Booking
from app.shuttle.models_orm import Shuttle, ShuttleLog
from app.key_management.models_orm import KeySlot, KeyMovement
from app.operators.models_orm import Operator


def get_dashboard_data(db: Session):
    """
    Ritorna la dashboard aggregata del parcheggio.

    Struttura di ritorno (stabile, pensata per il front-end):

    {
        "parking": {
            "areas": int,
            "spots_total": int,
            "spots_free": int,
            "spots_occupied": int,
            "spots_reserved": int,
            "utilization_rate": float | None
        },
        "bookings": {
            "total": int
        },
        "shuttle": {
            "vehicles": int,
            "logs": int,
            "last_log": {
                "id": int,
                "shuttle_id": int,
                "message": str,
                "timestamp": str
            } | None,
            "recent_logs": [
                {
                    "id": int,
                    "shuttle_id": int,
                    "message": str,
                    "timestamp": str
                },
                ...
            ]
        },
        "key_management": {
            "keyslots": int,
            "movements": int
        },
        "operators": {
            "total": int
        },
        "meta": {
            "generated_at": str
        }
    }
    """

    # ---------------------------------------------------------
    # PARKING
    # ---------------------------------------------------------
    areas = db.query(ParkingArea).count()

    spots_total = db.query(ParkingSpot).count()
    spots_free = db.query(ParkingSpot).filter(ParkingSpot.status == SpotStatus.FREE).count()
    spots_occupied = db.query(ParkingSpot).filter(ParkingSpot.status == SpotStatus.OCCUPIED).count()
    spots_reserved = db.query(ParkingSpot).filter(ParkingSpot.status == SpotStatus.RESERVED).count()

    utilization_rate = None
    if spots_total > 0:
        utilization_rate = spots_occupied / spots_total

    # ---------------------------------------------------------
    # BOOKINGS
    # ---------------------------------------------------------
    bookings_total = db.query(Booking).count()

    # ---------------------------------------------------------
    # SHUTTLE
    # ---------------------------------------------------------
    shuttles_total = db.query(Shuttle).count()
    shuttle_logs_total = db.query(ShuttleLog).count()

    last_log_obj = (
        db.query(ShuttleLog)
        .order_by(ShuttleLog.timestamp.desc())
        .first()
    )

    last_log = None
    if last_log_obj:
        last_log = {
            "id": last_log_obj.id,
            "shuttle_id": last_log_obj.shuttle_id,
            "message": last_log_obj.message,
            "timestamp": last_log_obj.timestamp.isoformat() if last_log_obj.timestamp else None,
        }

    recent_logs_objs = (
        db.query(ShuttleLog)
        .order_by(ShuttleLog.timestamp.desc())
        .limit(10)
        .all()
    )

    recent_logs = [
        {
            "id": log.id,
            "shuttle_id": log.shuttle_id,
            "message": log.message,
            "timestamp": log.timestamp.isoformat() if log.timestamp else None,
        }
        for log in recent_logs_objs
    ]

    # ---------------------------------------------------------
    # KEY MANAGEMENT
    # ---------------------------------------------------------
    keyslots_total = db.query(KeySlot).count()
    key_movements_total = db.query(KeyMovement).count()

    # ---------------------------------------------------------
    # OPERATORS
    # ---------------------------------------------------------
    operators_total = db.query(Operator).count()

    # ---------------------------------------------------------
    # META
    # ---------------------------------------------------------
    generated_at = datetime.now().isoformat()

    # ---------------------------------------------------------
    # RESPONSE
    # ---------------------------------------------------------
    return {
        "parking": {
            "areas": areas,
            "spots_total": spots_total,
            "spots_free": spots_free,
            "spots_occupied": spots_occupied,
            "spots_reserved": spots_reserved,
            "utilization_rate": utilization_rate,
        },
        "bookings": {
            "total": bookings_total,
        },
        "shuttle": {
            "vehicles": shuttles_total,
            "logs": shuttle_logs_total,
            "last_log": last_log,
            "recent_logs": recent_logs,
        },
        "key_management": {
            "keyslots": keyslots_total,
            "movements": key_movements_total,
        },
        "operators": {
            "total": operators_total,
        },
        "meta": {
            "generated_at": generated_at,
        },
    }
