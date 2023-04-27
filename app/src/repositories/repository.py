"""
"""

from typing import Dict, Optional
from abc import ABC, abstractmethod

from app.src.models import Car


class Repository(ABC):
    """
    """

    @abstractmethod
    def create_car(self, car: Car) -> None:
        """
        """

    @abstractmethod
    def read_all_cars(self) -> Optional[Dict[int, Car]]:
        """
        """

    @abstractmethod
    def read_car_by_id(self, car_id: int) -> Optional[Car]:
        """
        """

    @abstractmethod
    def update_car(self, car_id: int, car: Car) -> bool:
        """
        """

    @abstractmethod
    def delete_car(self, car_id: int) -> bool:
        """
        """
