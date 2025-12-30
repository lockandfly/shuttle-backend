# ============================
# Lock&Fly Backend Makefile (Pro)
# ============================

# Variabili
PYTHON=.venv/bin/python
UVICORN=$(PYTHON) -m uvicorn app.main:app --host 0.0.0.0 --port=8000

# ----------------------------
# AVVIO SERVER
# ----------------------------

# Avvio con reload (sviluppo attivo)
start:
	pkill -f uvicorn || true
	pkill -f python || true
	$(UVICORN) --reload

# Avvio stabile senza reload (test, demo, produzione)
safe-start:
	pkill -f uvicorn || true
	pkill -f python || true
	$(UVICORN)

# Arresta tutti i processi uvicorn/python
stop:
	pkill -f uvicorn || true
	pkill -f python || true

# Riavvio rapido
restart: stop start

# Avvio in background (non blocca il terminale)
start-bg:
	pkill -f uvicorn || true
	pkill -f python || true
	nohup $(UVICORN) --reload > uvicorn.log 2>&1 &

# Visualizza i log del server
logs:
	tail -f uvicorn.log

# ----------------------------
# AMBIENTE & DIPENDENZE
# ----------------------------

# Installa requirements
install:
	$(PYTHON) -m pip install -r requirements.txt

# Aggiorna pip
upgrade-pip:
	$(PYTHON) -m pip install --upgrade pip

# ----------------------------
# QUALITÀ DEL CODICE
# ----------------------------

# Formattazione automatica
format:
	$(PYTHON) -m black app

# Linting (controllo qualità)
lint:
	$(PYTHON) -m flake8 app || true

# ----------------------------
# PULIZIA
# ----------------------------

# Pulizia totale (processi + log + cache Python)
clean:
	pkill -f uvicorn || true
	pkill -f python || true
	rm -f uvicorn.log || true
	find . -type d -name "__pycache__" -exec rm -r {} + || true
	find . -type f -name "*.pyc" -delete || true
