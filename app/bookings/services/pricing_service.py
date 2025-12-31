from datetime import datetime


class PricingService:

    @staticmethod
    def calculate_price(arrival_time: datetime,
                        departure_time: datetime,
                        passenger_count: int = 1,
                        portal: str = "direct",
                        parking_area: str = "standard"):

        # Durata in ore
        duration_hours = (departure_time - arrival_time).total_seconds() / 3600

        # Prezzo base orario
        base_rate = 2.0

        # Sovrapprezzo passeggeri
        passenger_extra = max(0, passenger_count - 1) * 1.5

        # Sovrapprezzo area
        area_extra = 3.0 if parking_area == "covered" else 0.0

        # Sovrapprezzo portale
        portal_fee = 2.0 if portal != "direct" else 0.0

        final_price = (duration_hours * base_rate) + passenger_extra + area_extra + portal_fee

        return {
            "duration_hours": duration_hours,
            "base_rate": base_rate,
            "passenger_extra": passenger_extra,
            "area_extra": area_extra,
            "portal_fee": portal_fee,
            "final_price": round(final_price, 2)
        }
