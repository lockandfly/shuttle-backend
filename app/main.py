from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

# ====== ROUTER DATABASE ======
from app.routers import bookings_db

# ====== ROUTER IMPORT PRENOTAZIONI ======
from app.bookings.router import router as bookings_import_router


# ====== INIZIALIZZAZIONE FASTAPI ======
app = FastAPI(title="Lock&Fly Shuttle & Booking API")


# ====== CORS ======
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ====== ROOT ======
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


# ====== ROUTER DATABASE ======
app.include_router(bookings_db.router)

# ====== ROUTER IMPORT ======
app.include_router(bookings_import_router)
