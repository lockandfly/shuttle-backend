from fastapi import APIRouter

router = APIRouter(
    prefix="/db/bookings",
    tags=["Database Bookings"]
)

@router.get("/")
def list_bookings_db():
    return {"message": "Endpoint DB attivo, in attesa di implementazione"}
