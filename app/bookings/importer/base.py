from abc import ABC, abstractmethod
from app.schemas import BookingRead


class BaseImporter(ABC):
    """
    Classe base per tutti gli importer.
    Ogni importer deve implementare parse_row e restituire un BookingRead.
    """

    @staticmethod
    @abstractmethod
    def parse_row(row: dict) -> BookingRead:
        """
        Converte una riga del portale in un BookingRead.
        """
        pass
