def detect_service_type(description: str) -> str:
    if not description:
        return "standard"

    desc = description.lower()

    if "coperto" in desc or "covered" in desc:
        return "covered"

    if "scoperto" in desc or "uncovered" in desc:
        return "uncovered"

    if "vip" in desc:
        return "vip"

    return "standard"
