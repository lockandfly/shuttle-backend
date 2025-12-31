from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

# Routers modulari
from app.routers_modular.bookings_router import router as bookings_router
from app.routers_modular.parking_router import router as parking_area_router
from app.routers_modular.parking_spot_router import router as parking_spot_router
from app.routers_modular.shuttle_router import router as shuttle_router
from app.routers_modular.shuttle_movement_router import router as shuttle_movement_router
from app.routers_modular.key_management_router import router as key_management_router
from app.routers_modular.operators_router import router as operators_router
from app.routers_modular.pricing_router import router as pricing_router
from app.routers_modular.planner_router import router as planner_router
from app.routers_modular.occupancy_router import router as occupancy_router

# Crea tabelle se non esistono
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Lock&Fly Backend",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# ROUTERS
# -----------------------------

app.include_router(bookings_router, prefix="/bookings")
app.include_router(parking_area_router, prefix="/parking")
app.include_router(parking_spot_router, prefix="/parking")
app.include_router(shuttle_router, prefix="/shuttle")
app.include_router(shuttle_movement_router, prefix="/shuttle-movements")
app.include_router(key_management_router, prefix="/key-management")
app.include_router(operators_router, prefix="/operators")
app.include_router(pricing_router, prefix="/pricing")
app.include_router(planner_router, prefix="/planner")
app.include_router(occupancy_router, prefix="/occupancy")

@app.get("/")
def root():
    return {"status": "ok", "service": "Lock&Fly Backend"}
