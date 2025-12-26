import pandas as pd
import uuid
from datetime import datetime
import os


class BookingManager:
    def __init__(self, filename="bookings.csv"):
        self.filename = filename
        if not os.path.exists(self.filename):
            df = pd.DataFrame(columns=[
                "Id",
                "CustomerName",
                "Phone",
                "Email",
                "Plate",
                "ArrivalDate",
                "ArrivalTime",
                "ReturnDate",
                "ReturnTime",
                "People",
                "ServiceType",
                "ShuttleId",
                "Notes",
            ])
            df.to_csv(self.filename, index=False)

    def load_data(self):
        return pd.read_csv(self.filename, dtype=str).fillna("")

    def save_data(self, df):
        df.to_csv(self.filename, index=False)

    def _validate_date(self, date_str, field_name="Data"):
        if not date_str:
            raise ValueError(f"{field_name} obbligatoria (gg/mm/aaaa).")
        try:
            d = datetime.strptime(date_str, "%d/%m/%Y")
            return d.strftime("%d/%m/%Y")
        except Exception:
            raise ValueError(f"{field_name} non valida. Usa gg/mm/aaaa.")

    def _validate_time(self, time_str, field_name="Ora"):
        if not time_str:
            raise ValueError(f"{field_name} obbligatoria (HH:MM).")
        try:
            t = datetime.strptime(time_str, "%H:%M")
            return t.strftime("%H:%M")
        except Exception:
            raise ValueError(f"{field_name} non valida. Usa HH:MM.")

    def _clean_str(self, value):
        return str(value).strip() if value is not None else ""

    def _validate_people(self, people):
        if people in (None, ""):
            return ""
        try:
            n = int(people)
            if n < 0:
                raise ValueError("Numero persone non può essere negativo.")
            return str(n)
        except Exception:
            raise ValueError("Numero persone non valido.")

    def add_booking(
        self,
        customer_name,
        phone,
        email,
        plate,
        arrival_date,
        arrival_time,
        return_date,
        return_time,
        people,
        service_type,
        shuttle_id="",
        notes="",
    ):
        df = self.load_data()

        customer_name = self._clean_str(customer_name)
        if not customer_name:
            raise ValueError("Il nome cliente è obbligatorio.")

        phone = self._clean_str(phone)
        email = self._clean_str(email)
        plate = self._clean_str(plate)

        arrival_date = self._validate_date(arrival_date, "Data arrivo")
        arrival_time = self._validate_time(arrival_time, "Ora arrivo")
        return_date = self._validate_date(return_date, "Data rientro")
        return_time = self._validate_time(return_time, "Ora rientro")

        people = self._validate_people(people)
        service_type = self._clean_str(service_type)
        shuttle_id = self._clean_str(shuttle_id)
        notes = self._clean_str(notes)

        new_id = str(uuid.uuid4())
        new_row = {
            "Id": new_id,
            "CustomerName": customer_name,
            "Phone": phone,
            "Email": email,
            "Plate": plate,
            "ArrivalDate": arrival_date,
            "ArrivalTime": arrival_time,
            "ReturnDate": return_date,
            "ReturnTime": return_time,
            "People": people,
            "ServiceType": service_type,
            "ShuttleId": shuttle_id,
            "Notes": notes,
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        self.save_data(df)
        return new_row

    def get_bookings(self, date=None):
        df = self.load_data()
        if date:
            try:
                d = self._validate_date(date, "Data filtro")
                df = df[df["ArrivalDate"] == d]
            except Exception:
                return []
        return df.to_dict(orient="records")

    def get_booking(self, booking_id):
        df = self.load_data()
        if booking_id not in df["Id"].values:
            return None
        row = df[df["Id"] == booking_id].iloc[0]
        return row.to_dict()

    def update_booking(
        self,
        booking_id,
        customer_name=None,
        phone=None,
        email=None,
        plate=None,
        arrival_date=None,
        arrival_time=None,
        return_date=None,
        return_time=None,
        people=None,
        service_type=None,
        shuttle_id=None,
        notes=None,
    ):
        df = self.load_data()
        if booking_id not in df["Id"].values:
            return None
        idx = df.index[df["Id"] == booking_id][0]

        if customer_name is not None:
            df.at[idx, "CustomerName"] = self._clean_str(customer_name)
        if phone is not None:
            df.at[idx, "Phone"] = self._clean_str(phone)
        if email is not None:
            df.at[idx, "Email"] = self._clean_str(email)
        if plate is not None:
            df.at[idx, "Plate"] = self._clean_str(plate)
        if arrival_date is not None:
            df.at[idx, "ArrivalDate"] = self._validate_date(arrival_date, "Data arrivo")
        if arrival_time is not None:
            df.at[idx, "ArrivalTime"] = self._validate_time(arrival_time, "Ora arrivo")
        if return_date is not None:
            df.at[idx, "ReturnDate"] = self._validate_date(return_date, "Data rientro")
        if return_time is not None:
            df.at[idx, "ReturnTime"] = self._validate_time(return_time, "Ora rientro")
        if people is not None:
            df.at[idx, "People"] = self._validate_people(people)
        if service_type is not None:
            df.at[idx, "ServiceType"] = self._clean_str(service_type)
        if shuttle_id is not None:
            df.at[idx, "ShuttleId"] = self._clean_str(shuttle_id)
        if notes is not None:
            df.at[idx, "Notes"] = self._clean_str(notes)

        self.save_data(df)
        return df.loc[idx].to_dict()

    def delete_booking(self, booking_id):
        df = self.load_data()
        if booking_id not in df["Id"].values:
            return None
        df = df[df["Id"] != booking_id]
        self.save_data(df)
        return {"deleted": booking_id}

    def get_dataframe(self, date=None):
        df = self.load_data()
        if date:
            try:
                d = self._validate_date(date, "Data filtro")
                df = df[df["ArrivalDate"] == d]
            except Exception:
                return pd.DataFrame(columns=df.columns)
        return df
