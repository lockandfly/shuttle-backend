from fastapi import APIRouter, UploadFile, File
import pandas as pd
import shutil
import os

router = APIRouter(prefix="/import", tags=["Import Preview"])

@router.post("/preview")
async def preview_file(file: UploadFile = File(...)):
    """
    Restituisce le prime 5 righe del file CSV/XLSX caricato.
    Utile per verificare che il file sia corretto prima dell'import.
    """

    temp_path = f"/tmp/{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        if temp_path.endswith(".csv"):
            df = pd.read_csv(temp_path)
        else:
            df = pd.read_excel(temp_path)

        preview = df.head(5).to_dict(orient="records")

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return {
        "rows": len(df),
        "preview": preview
    }
