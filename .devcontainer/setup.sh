#!/bin/bash

echo "[SETUP] Creazione virtualenv..."
python3 -m venv /workspaces/shuttle-backend/.venv

echo "[SETUP] Attivazione virtualenv..."
source /workspaces/shuttle-backend/.venv/bin/activate

echo "[SETUP] Aggiornamento pip..."
pip install --upgrade pip

echo "[SETUP] Installazione requirements..."
pip install -r /workspaces/shuttle-backend/requirements.txt

echo "[SETUP] Configurazione completata."
