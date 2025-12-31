class ImportValidator:

    @staticmethod
    def require_columns(df, required, portal):
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise ValueError(
                f"Il file del portale '{portal}' non contiene le colonne obbligatorie: {missing}"
            )

    @staticmethod
    def require_non_empty(df, portal):
        if df.empty:
            raise ValueError(f"Il file del portale '{portal}' è vuoto.")
