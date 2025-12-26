import pandas as pd
import uuid
from datetime import datetime
import os


class ShuttleScheduler:
    def __init__(self, filename="shuttles.csv"):
        self.filename = filename
        if not os.path.exists(self.filename):
            df = pd.DataFrame(columns=["Id", "Date", "Time", "Destination"])
            df.to_csv(self.filename, index=False)

    def load_data(self):
        return pd.read_csv(self.filename)

    def save_data(self, df):
        df.to_csv(self.filename, index=False)

    def validate_date(self, date_str):
        try:
            d = datetime.strptime(date_str, "%d/%m/%Y")
            return d.strftime("%d/%m/%Y")
        except Exception:
            raise ValueError("Formato data non valido. Usa gg/mm/aaaa.")

    def validate_time(self, time_str):
        if not time_str:
            raise ValueError("L'ora è obbligatoria.")
        try:
            t = datetime.strptime(time_str, "%H:%M")
            return t.strftime("%H:%M")
        except Exception:
            raise ValueError("Formato ora non valido. Usa HH:MM.")

    def validate_destination(self, dest):
        if not dest or len(str(dest).strip()) == 0:
            raise ValueError("La destinazione è obbligatoria.")
        return str(dest).strip()

    def add_shuttle(self, date_str, time_str, destination):
        df = self.load_data()

        d = self.validate_date(date_str)
        t = self.validate_time(time_str)
        dest = self.validate_destination(destination)

        new_id = str(uuid.uuid4())
        new_row = {"Id": new_id, "Date": d, "Time": t, "Destination": dest}

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        self.save_data(df)
        return new_row

    def get_shuttles(self, date=None):
        df = self.load_data()
        if date:
            try:
                d = self.validate_date(date)
                df = df[df["Date"] == d]
            except Exception:
                return []
        return df.to_dict(orient="records")

    def update_shuttle(self, shuttle_id, date=None, time=None, destination=None):
        df = self.load_data()
        if shuttle_id not in df["Id"].values:
            return None
        idx = df.index[df["Id"] == shuttle_id][0]
        if date:
            df.at[idx, "Date"] = self.validate_date(date)
        if time:
            df.at[idx, "Time"] = self.validate_time(time)
        if destination:
            df.at[idx, "Destination"] = self.validate_destination(destination)
        self.save_data(df)
        return df.loc[idx].to_dict()

    def delete_shuttle(self, shuttle_id):
        df = self.load_data()
        if shuttle_id not in df["Id"].values:
            return None
        df = df[df["Id"] != shuttle_id]
        self.save_data(df)
        return {"deleted": shuttle_id}

    def get_dataframe(self, date=None):
        df = self.load_data()
        if date:
            try:
                d = self.validate_date(date)
                df = df[df["Date"] == d]
            except Exception:
                return pd.DataFrame(columns=["Id", "Date", "Time", "Destination"])
        return df
