import os
from typing import List

import pandas as pd
from fastapi import HTTPException

from app.portals.enums import Portal


class ImportDetectionService:

    @staticmethod
    def _read_file_to_dataframe(file_path: str) -> pd.DataFrame:
        """
        Legge il file in un DataFrame pandas, gestendo sia CSV che XLSX.
        """
        extension = os.path.splitext(file_path)[1].lower()

        try:
            if extension == ".csv":
                df = pd.read_csv(file_path)
            elif extension in [".xlsx", ".xls"]:
                df = pd.read_excel(file_path)
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Formato file non supportato: {extension}",
                )
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Errore lettura file: {str(e)}")

        if df.empty:
            raise HTTPException(status_code=400, detail="Il file è vuoto")

        return df

    @staticmethod
    def _normalize_columns(columns: List[str]) -> List[str]:
        """
        Normalizza i nomi delle colonne per facilitare il matching.
        """
        return [str(c).strip().lower() for c in columns]

    @staticmethod
    def detect_portal_from_file(file_path: str) -> Portal:
        """
        Tenta di riconoscere il portale dal contenuto del file.
        Usa:
        - estensione (.csv vs .xlsx)
        - nomi delle colonne tipiche per ciascun portale
        """
        df = ImportDetectionService._read_file_to_dataframe(file_path)
        columns = ImportDetectionService._normalize_columns(list(df.columns))

        extension = os.path.splitext(file_path)[1].lower()

        # 1) MyParking: tipicamente XLSX con colonne italiane tipo "Nominativo", "Ingresso", "Uscita"
        if extension in [".xlsx", ".xls"]:
            if any("nominativo" in c for c in columns) and any("ingresso" in c for c in columns):
                return Portal.myparking

        # 2) ParkingMyCar: CSV, con colonne come "Cliente", "Dettagli Veicolo", "Check-in", "Check-out"
        if extension == ".csv":
            has_cliente = any("cliente" in c for c in columns)
            has_dettagli_veicolo = any("dettagli veicolo" in c or "dettagli_veicolo" in c for c in columns)
            has_checkin = any("check-in" in c or "check in" in c or "checkin" in c for c in columns)
            has_checkout = any("check-out" in c or "check out" in c or "checkout" in c for c in columns)

            if has_cliente and has_dettagli_veicolo and has_checkin and has_checkout:
                return Portal.parkingmycar

        # 3) Parkos: CSV, con colonne come "Nome", "Ingresso", "Uscita", "Email", "Telefono"
        if extension == ".csv":
            has_nome = any(c == "nome" or "nome" in c for c in columns)
            has_ingresso = any("ingresso" in c for c in columns)
            has_uscita = any("uscita" in c for c in columns)

            if has_nome and has_ingresso and has_uscita:
                return Portal.parkos

        # Se non riconosciamo il formato:
        raise HTTPException(
            status_code=400,
            detail="Impossibile riconoscere automaticamente il portale dal file. Verifica il formato o il template.",
        )
