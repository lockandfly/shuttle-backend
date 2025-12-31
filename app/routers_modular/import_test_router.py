from fastapi import APIRouter
from app.bookings.services.import_service import ImportService

router = APIRouter(prefix="/import", tags=["Import Test"])

@router.post("/test")
def test_parser(portal: str, row: dict):
    """
    Testa un parser senza caricare file.
    row = dict con i campi del portale.
    """

    parser_map = {
        "parkos": ImportService.parse_parkos,
        "myparking": ImportService.parse_myparking,
        "parkingmycar": ImportService.parse_parkingmycar,
        "lockandfly": ImportService.parse_lockandfly,
    }

    if portal not in parser_map:
        return {"error": "Portale non supportato"}

    parser = parser_map[portal]

    import pandas as pd
    row_series = pd.Series(row)

    result = parser(row_series)

    return {"parsed": result}
