.PHONY: start stop install logs

start:
    uvicorn app.main:app --host 0.0.0.0 --port=8000 --reload

stop:
    pkill -f "uvicorn" || true

install:
    source .venv/bin/activate && pip install -r requirements.txt

logs:
    tail -f logs/backend.log