import re

def normalize_license_plate(plate: str) -> str:
    if not plate:
        return ""
    plate = plate.strip().upper()
    plate = re.sub(r"[^A-Z0-9]", "", plate)
    return plate


def normalize_name(name: str) -> str:
    if not name:
        return ""
    name = name.strip()
    name = " ".join(name.split())
    return name.title()
