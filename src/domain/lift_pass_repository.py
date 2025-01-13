from abc import ABC, abstractmethod

from src.domain.lift_pass import LiftPass
from src.domain.lift_pass_type import LiftPassType


class LiftPassRepository(ABC):
    @abstractmethod
    def save(self, lift_pass: LiftPass) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, pass_type: LiftPassType) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by(self, pass_type: LiftPassType) -> LiftPass:
        raise NotImplementedError
