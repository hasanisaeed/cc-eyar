from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import OrderEntity


class OrderRepositoryInterface(ABC):
    @abstractmethod
    def save(self, order: OrderEntity) -> OrderEntity:
        pass

    @abstractmethod
    def get_by_id(self, order_id: int) -> Optional[OrderEntity]:
        pass

    @abstractmethod
    def list_all(self, filters: dict) -> List[OrderEntity]:
        pass

    @abstractmethod
    def delete(self, order_id: int) -> None:
        pass
