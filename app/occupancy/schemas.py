from pydantic import BaseModel


class OccupancyResponse(BaseModel):
    total_spots: int
    occupied_spots: int
    free_spots: int
    occupancy_rate: float
