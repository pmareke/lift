from abc import ABC, abstractmethod


class LiftPassCost(ABC):
    @abstractmethod
    def cost(self, *args, **kwargs) -> float:
        raise NotImplementedError
