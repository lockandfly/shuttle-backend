def _normalize(self, value):
    if value is None:
        return ""
    return (
        str(value)
        .strip()
        .lower()
        .replace("\xa0", " ")
        .replace("\n", " ")
        .replace("\t", " ")
        .replace("\ufeff", "")  # ← rimuove BOM
    )
