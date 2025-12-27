#!/bin/bash

echo "[Startup] Attivazione ambiente virtuale..."

if [ ! -d "/workspaces/shuttle-backend/.venv" ]; then
    python3 -m venv /workspaces/shuttle-backend/.venv
fi

source /workspaces/shuttle-backend/.venv/bin/activate

echo "[Startup] Installazione dipendenze..."
pip install --upgrade pip
pip install -r /workspaces/shuttle-backend/requirements.txt

echo "[Startup] Completato. Avvia FastAPI manualmente con:"
echo "uvicorn app.main:app --host 0.0.0.0 --port=8000 --reload"
