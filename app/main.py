from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.bookings.router import router as bookings_router

# Crea le tabelle se non esistono
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Lock&Fly Backend",
    description="Backend operativo per gestione prenotazioni, navette, dashboard e ottimizzazioni",
    version="1.0.0"
)

# -------------------------
# CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # puoi restringerlo in produzione
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# ROUTERS
# -------------------------
app.include_router(bookings_router, prefix="/bookings", tags=["Bookings"])

# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/health")
def health():
    return {"status": "ok", "service": "Lock&Fly Backend"}

