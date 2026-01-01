from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, JSON
from sqlalchemy.sql import func
from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    # Identificativo portale (parkos, myparking, direct, parkingmycar)
    portal = Column(String, index=True, nullable=False)

    # Campi normalizzati Parkos / portali
    code = Column(String, nullable=True)
    customer_name = Column(String, nullable=True)
    customer_email = Column(String, nullable=True)

    # Telefono principale (versione "semplice")
    phone = Column(String, nullable=True)

    # Telefono cliente (versione avanzata / portali)
    customer_phone = Column(String, nullable=True)

    license_plate = Column(String, nullable=True)

    # Date normalizzate
    arrival = Column(DateTime, nullable=False)
    departure = Column(DateTime, nullable=False)

    # Date avanzate (compatibili con vecchi importer)
    arrival_time = Column(DateTime, nullable=True)
    departure_time = Column(DateTime, nullable=True)

    # Prezzo semplice (versione base)
    price = Column(Float, nullable=True)

    # Flag pagamento e informazioni esterne
    payment_complete = Column(Boolean, nullable=True)
    external_id = Column(String, nullable=True)
    online_payment = Column(Boolean, nullable=True)
    payment_option = Column(String, nullable=True)

    # Dati cancellazione
    cancel_date = Column(DateTime, nullable=True)
    cancel_reason = Column(String, nullable=True)

    # Passeggeri e giorni (versione semplice)
    passengers = Column(Integer, nullable=True)
    days = Column(Integer, nullable=True)

    # Conteggio passeggeri (versione avanzata / compatibilità importer)
    passenger_count = Column(Integer, nullable=True)

    # Campo interno note
    notes = Column(String, nullable=True)

    # -----------------------------
    # CAMPI AVANZATI PER DYNAMIC PRICING / PORTALI
    # -----------------------------

    # Area di parcheggio / tipo servizio (es. shuttle, car valet, coperto, scoperto)
    parking_area = Column(String, nullable=True)

    # Prezzo base (prima degli aggiustamenti dinamici)
    base_price = Column(Float, nullable=True)

    # Prezzo finale (dopo dynamic pricing)
    final_price = Column(Float, nullable=True)

    # Dettaglio aggiustamenti (JSON: elenco regole applicate)
    pricing_breakdown = Column(JSON, nullable=True)

    # Spiegazione testuale delle regole applicate
    pricing_reasoning = Column(String, nullable=True)

    # Stato prenotazione (active, cancelled, no_show, ecc.)
    status = Column(String, nullable=True)

    # Dati grezzi dell'import (row del portale, serializzata)
    raw_data = Column(JSON, nullable=True)

    # Timestamp automatici
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
