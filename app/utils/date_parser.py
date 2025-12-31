from datetime import datetime

def parse_date(value: str):
    if not value:
        return None

    value = value.strip()

    formats = [
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%d-%m-%Y %H:%M",
        "%d-%m-%Y",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except:
            pass

    # fallback: try ISO
    try:
        return datetime.fromisoformat(value)
    except:
        return None
from datetime import datetime

def parse_date(value: str):
    if not value:
        return None

    value = value.strip()

    formats = [
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%d-%m-%Y %H:%M",
        "%d-%m-%Y",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except:
            pass

    # fallback: try ISO
    try:
        return datetime.fromisoformat(value)
    except:
        return None
