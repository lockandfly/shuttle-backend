from abc import ABC, abstractmethod
from typing import List
from app.bookings.models import BookingCreate

class BaseImporter(ABC):

    @abstractmethod
    def parse(self, file_path: str) -> List[BookingCreate]:
        ...
