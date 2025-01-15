from abc import ABC, abstractmethod


class LiftPassCost(ABC):
    @abstractmethod
    def calculate(self) -> float:
        raise NotImplementedError
