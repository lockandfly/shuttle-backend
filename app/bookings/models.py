from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    # Portale di provenienza (parkos, myparking, parkingmycar, lockandfly)
    portal = Column(String, index=True, nullable=False)

    # Dati cliente
    customer_name = Column(String, nullable=False)
    customer_email = Column(String, nullable=True)

    # Targa
    license_plate = Column(String, nullable=True)

    # Date
    arrival = Column(DateTime, nullable=False)
    departure = Column(DateTime, nullable=False)

    # Prezzo
    price = Column(Float, nullable=False)

    # Note varie (stato, area sosta, parcheggio, ecc.)
    notes = Column(String, nullable=True)
