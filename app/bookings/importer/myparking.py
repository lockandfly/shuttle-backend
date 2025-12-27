import openpyxl
from datetime import datetime
from app.bookings.models import BookingCreate, BookingRead


class MyParkingImporter:
    COLUMN_MAP = {
        "reservation_id": ["Codice Prenotazione"],
        "checkin": ["Ingresso"],
        "checkout": ["Uscita"],
        "customer_name": ["Nominativo", "Cliente"],
        "car_plate": ["Targa"],
        "price": [
            "Da pagare", "Da pagare in parcheggio",
            "Pagato online", "Pagato", "online",
            "Importo", "Totale", "Totale online"
        ],
    }

    def _normalize(self, value):
        if value is None:
            return ""
        return str(value).strip().lower().replace("\xa0", " ").replace("\n", " ").replace("\t", " ")

    def _find_column(self, header_row, possible_names):
        normalized = [self._normalize(cell.value) for cell in header_row]

        # Caso speciale: 'Pagato' + 'online' separati
        if "pagato" in normalized and "online" in normalized:
            if "Pagato online" in possible_names or "Pagato" in possible_names:
                return ("split", normalized.index("pagato"), normalized.index("online"))

        for idx, cell in enumerate(header_row):
            cell_value = self._normalize(cell.value)
            for name in possible_names:
                if cell_value == name.lower():
                    return idx

        print("Intestazioni trovate:", normalized)
        raise KeyError(possible_names[0])

    def _parse_price(self, row, col_price):
        if isinstance(col_price, tuple) and col_price[0] == "split":
            _, idx1, idx2 = col_price
            raw = f"{row[idx1] or ''}{row[idx2] or ''}"
        else:
            raw = row[col_price]

        if raw is None:
            return 0.0

        if isinstance(raw, str):
            raw = raw.replace("€", "").replace(",", ".").strip()

        try:
            return float(raw)
        except:
            return 0.0

    def _simulate_response(self, bookings):
        now = datetime.utcnow()
        return [
            BookingRead(
                id=f"imported-{b.portal_reservation_id}",
                portal=b.portal,
                portal_reservation_id=b.portal_reservation_id,
                customer_name=b.customer_name,
                email=b.email,
                phone=b.phone,
                checkin=b.checkin,
                checkout=b.checkout,
                car_plate=b.car_plate,
                price=b.price,
                created_at=now,
                updated_at=now,
            )
            for b in bookings
        ]

    def parse(self, file):
        wb = openpyxl.load_workbook(file, data_only=True)
        sheet = wb.active
        header = list(sheet[1])

        col = {}
        for key, variants in self.COLUMN_MAP.items():
            col[key] = self._find_column(header, variants)

        raw_bookings = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            if not any(row):
                continue

            try:
                checkin = row[col["checkin"]]
                checkout = row[col["checkout"]]

                if isinstance(checkin, str):
                    checkin = datetime.strptime(checkin, "%d/%m/%Y %H:%M")
                if isinstance(checkout, str):
                    checkout = datetime.strptime(checkout, "%d/%m/%Y %H:%M")

                price = self._parse_price(row, col["price"])
                car_plate = row[col["car_plate"]] if row[col["car_plate"]] else ""

                booking = BookingCreate(
                    portal="MyParking",
                    portal_reservation_id=str(row[col["reservation_id"]]),
                    customer_name=row[col["customer_name"]],
                    email="",
                    phone="",
                    checkin=checkin,
                    checkout=checkout,
                    car_plate=car_plate,
                    price=price,
                )

                raw_bookings.append(booking)

            except Exception as e:
                print("Errore riga:", row)
                raise e

        return self._simulate_response(raw_bookings)
