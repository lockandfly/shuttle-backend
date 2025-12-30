#!/bin/bash

PROJECT_DIR="/workspaces/shuttle-backend"
VENV_DIR="$PROJECT_DIR/.venv"

echo "[Lock&Fly] Avvio automatico ambiente…"

# 1) Crea il venv se non esiste
if [ ! -d "$VENV_DIR" ]; then
    echo "[Lock&Fly] Nessun venv trovato. Lo creo ora…"
    python3 -m venv "$VENV_DIR"
fi

# 2) Attiva il venv
echo "[Lock&Fly] Attivo il venv…"
source "$VENV_DIR/bin/activate"

# 3) Installa requirements se mancano
if [ ! -f "$VENV_DIR/.requirements_installed" ]; then
    echo "[Lock&Fly] Installo requirements…"
    pip install --upgrade pip
    pip install -r "$PROJECT_DIR/requirements.txt"
    touch "$VENV_DIR/.requirements_installed"
else
    echo "[Lock&Fly] Requirements già installati."
fi

# 4) NON avviare FastAPI automaticamente
echo "[Lock&Fly] Ambiente pronto. Avvia FastAPI manualmente con:"
echo "uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

exit 0
