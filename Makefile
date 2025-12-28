# ============================
# Lock&Fly Backend Makefile
# ============================

# Avvio con reload (sviluppo attivo)
start:
	pkill -f uvicorn || true
	pkill -f python || true
	python -m uvicorn app.main:app --host 0.0.0.0 --port=8000 --reload

# Avvio stabile senza reload (test, demo, produzione)
safe-start:
	pkill -f uvicorn || true
	pkill -f python || true
	python -m uvicorn app.main:app --host 0.0.0.0 --port=8000

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
	nohup python -m uvicorn app.main:app --host 0.0.0.0 --port=8000 --reload > uvicorn.log 2>&1 &

# Visualizza i log del server
logs:
	tail -f uvicorn.log

# Pulizia totale (processi + log)
clean:
	pkill -f uvicorn || true
	pkill -f python || true
	rm -f uvicorn.log || true
