from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers_modular.import_router import router as import_router
from app.routers_modular.bookings_router import router as bookings_router
from app.routers_modular.dashboard_router import router as dashboard_router
from app.routers_modular.occupancy_router import router as occupancy_router
from app.routers_modular.operators_router import router as operators_router
from app.routers_modular.parking_router import router as parking_router
from app.routers_modular.planner_router import router as planner_router
from app.routers_modular.portals_router import router as portals_router
from app.routers_modular.pricing_router import router as pricing_router
from app.routers_modular.shuttle_router import router as shuttle_router
from app.routers_modular.finance_router import router as finance_router
from app.routers_modular.optimizer_router import router as optimizer_router
from app.routers_modular.parking_spot_router import router as parking_spot_router
from app.routers_modular.pricing_calc_router import router as pricing_calc_router
from app.routers_modular.shuttle_movement_router import router as shuttle_movement_router
from app.routers_modular.import_logs_router import router as import_logs_router
from app.routers_modular.import_preview_router import router as import_preview_router
from app.routers_modular.import_test_router import router as import_test_router
from app.routers_modular.key_management_router import router as key_management_router

# ---------------------------------------------------------
# CREA TUTTE LE TABELLE DEL DATABASE
# ---------------------------------------------------------
Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------
# FASTAPI APP
# ---------------------------------------------------------
app = FastAPI(title="Shuttle Backend")

# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# ROUTERS
# ---------------------------------------------------------
app.include_router(import_router)
app.include_router(bookings_router)
app.include_router(dashboard_router)
app.include_router(occupancy_router)
app.include_router(operators_router)
app.include_router(parking_router)
app.include_router(planner_router)
app.include_router(portals_router)
app.include_router(pricing_router)
app.include_router(shuttle_router)
app.include_router(finance_router)
app.include_router(optimizer_router)
app.include_router(parking_spot_router)
app.include_router(pricing_calc_router)
app.include_router(shuttle_movement_router)
app.include_router(import_logs_router)
app.include_router(import_preview_router)
app.include_router(import_test_router)
app.include_router(key_management_router)
