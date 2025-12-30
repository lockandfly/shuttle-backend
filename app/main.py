from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

# Routers
from app.routers_modular.parking_router import router as parking_areas_router
from app.routers_modular.parking_spot_router import router as parking_spots_router
from app.routers_modular.bookings_router import router as bookings_router
from app.routers_modular.key_management_router import router as key_management_router
from app.routers_modular.operators_router import router as operators_router
from app.routers_modular.shuttle_router import router as shuttle_router
from app.routers_modular.dashboard_router import router as dashboard_router


# ---------------------------------------------------------
# APP INIT
# ---------------------------------------------------------

app = FastAPI(
    title="Lock&Fly Backend",
    version="1.0.0",
)


# ---------------------------------------------------------
# DATABASE INIT
# ---------------------------------------------------------

# Crea tutte le tabelle definite nei modelli ORM
Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------
# CORS (puoi restringerlo quando vai in produzione)
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in prod: metti i domini reali
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# ROUTERS
# ---------------------------------------------------------

# Parking Areas
app.include_router(
    parking_areas_router,
    prefix="/parking",
)

# Parking Spots
app.include_router(
    parking_spots_router,
    prefix="/parking/spots",
)

# Bookings
app.include_router(
    bookings_router,
    prefix="/bookings",
)

# Key Management
app.include_router(
    key_management_router,
    prefix="/key-management",
)

# Operators
app.include_router(
    operators_router,
    prefix="/operators",
)

# Shuttle
app.include_router(
    shuttle_router,
    prefix="/shuttle",
)

# Dashboard
app.include_router(
    dashboard_router,
    prefix="/dashboard",
)


# ---------------------------------------------------------
# ROOT ENDPOINT
# ---------------------------------------------------------

@app.get("/")
def root():
    return {"status": "ok", "message": "Lock&Fly backend is running"}
