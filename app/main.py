from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from typing import Optional, List

from shuttle_scheduler import ShuttleScheduler
from booking_manager import BookingManager

app = FastAPI(title="Lock&Fly Shuttle & Booking API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # puoi restringere in futuro
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = ShuttleScheduler("shuttles.csv")
booking_manager = BookingManager("bookings.csv")


# ====== MODELLI NAVETTE ======

class ShuttleCreate(BaseModel):
    date: str = Field(..., example="28/12/2025")
    time: str = Field(..., example="10:00")
    destination: str = Field(..., example="porto")


class ShuttleUpdate(BaseModel):
    date: Optional[str] = Field(None, example="28/12/2025")
    time: Optional[str] = Field(None, example="10:00")
    destination: Optional[str] = Field(None, example="porto")


# ====== MODELLI PRENOTAZIONI ======

class BookingCreate(BaseModel):
    customer_name: str = Field(..., example="Mario Rossi")
    phone: Optional[str] = Field(None, example="+39 333 1234567")
    email: Optional[str] = Field(None, example="cliente@example.com")
    plate: Optional[str] = Field(None, example="AB123CD")
    arrival_date: str = Field(..., example="28/12/2025")
    arrival_time: str = Field(..., example="10:00")
    return_date: str = Field(..., example="05/01/2026")
    return_time: str = Field(..., example="22:30")
    people: Optional[str] = Field(None, example="2")
    service_type: Optional[str] = Field(None, example="navetta")
    shuttle_id: Optional[str] = Field(None, example="uuid-navetta")
    notes: Optional[str] = Field(None, example="Cliente abituale")


class BookingUpdate(BaseModel):
    customer_name: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    plate: Optional[str] = Field(None)
    arrival_date: Optional[str] = Field(None)
    arrival_time: Optional[str] = Field(None)
    return_date: Optional[str] = Field(None)
    return_time: Optional[str] = Field(None)
    people: Optional[str] = Field(None)
    service_type: Optional[str] = Field(None)
    shuttle_id: Optional[str] = Field(None)
    notes: Optional[str] = Field(None)


# ====== ROOT ======

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


# ====== NAVETTE ENDPOINTS ======

@app.get("/shuttles", response_model=List[dict])
def list_shuttles(date: Optional[str] = Query(None, description="Filtro per data dd/mm/YYYY")):
    return scheduler.get_shuttles(date)


@app.post("/shuttles", response_model=dict)
def create_shuttle(payload: ShuttleCreate):
    try:
        return scheduler.add_shuttle(payload.date, payload.time, payload.destination)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/shuttles/{shuttle_id}", response_model=dict)
def update_shuttle(
    shuttle_id: str = Path(..., description="UUID navetta"),
    payload: ShuttleUpdate = None
):
    if payload is None:
        raise HTTPException(status_code=400, detail="Nessun payload fornito")

    try:
        updated = scheduler.update_shuttle(shuttle_id, payload.date, payload.time, payload.destination)
        if updated is None:
            raise HTTPException(status_code=404, detail="Navetta non trovata")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/shuttles/{shuttle_id}", response_model=dict)
def delete_shuttle(shuttle_id: str = Path(..., description="UUID navetta")):
    res = scheduler.delete_shuttle(shuttle_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Navetta non trovata")
    return res


@app.get("/report/xlsx")
def export_shuttles_xlsx(date: Optional[str] = Query(None, description="Filtro opzionale dd/mm/YYYY")):
    df = scheduler.get_dataframe(date)
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    return {
        "filename": f"shuttles_{date or 'all'}.csv",
        "content": csv_bytes.decode("utf-8")
    }


# ====== PRENOTAZIONI ENDPOINTS ======

@app.get("/bookings", response_model=List[dict])
def list_bookings(date: Optional[str] = Query(None, description="Filtra per data arrivo dd/mm/YYYY")):
    return booking_manager.get_bookings(date)


@app.post("/bookings", response_model=dict)
def create_booking(payload: BookingCreate):
    try:
        booking = booking_manager.add_booking(
            customer_name=payload.customer_name,
            phone=payload.phone,
            email=payload.email,
            plate=payload.plate,
            arrival_date=payload.arrival_date,
            arrival_time=payload.arrival_time,
            return_date=payload.return_date,
            return_time=payload.return_time,
            people=payload.people,
            service_type=payload.service_type,
            shuttle_id=payload.shuttle_id or "",
            notes=payload.notes or "",
        )
        return booking
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/bookings/{booking_id}", response_model=dict)
def get_booking(booking_id: str = Path(..., description="UUID prenotazione")):
    booking = booking_manager.get_booking(booking_id)
    if booking is None:
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")
    return booking


@app.put("/bookings/{booking_id}", response_model=dict)
def update_booking(
    booking_id: str = Path(..., description="UUID prenotazione"),
    payload: BookingUpdate = None
):
    if payload is None:
        raise HTTPException(status_code=400, detail="Nessun payload fornito")

    try:
        updated = booking_manager.update_booking(
            booking_id=booking_id,
            customer_name=payload.customer_name,
            phone=payload.phone,
            email=payload.email,
            plate=payload.plate,
            arrival_date=payload.arrival_date,
            arrival_time=payload.arrival_time,
            return_date=payload.return_date,
            return_time=payload.return_time,
            people=payload.people,
            service_type=payload.service_type,
            shuttle_id=payload.shuttle_id,
            notes=payload.notes,
        )
        if updated is None:
            raise HTTPException(status_code=404, detail="Prenotazione non trovata")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/bookings/{booking_id}", response_model=dict)
def delete_booking(booking_id: str = Path(..., description="UUID prenotazione")):
    res = booking_manager.delete_booking(booking_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")
    return res


@app.get("/bookings/report/xlsx")
def export_bookings_xlsx(date: Optional[str] = Query(None, description="Filtro opzionale dd/mm/YYYY su data arrivo")):
    df = booking_manager.get_dataframe(date)
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    return {
        "filename": f"bookings_{date or 'all'}.csv",
        "content": csv_bytes.decode("utf-8")
    }
