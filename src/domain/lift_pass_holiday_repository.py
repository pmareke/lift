from abc import ABC, abstractmethod


class LiftPassHolidayRepository(ABC):
    @abstractmethod
    def is_holiday(self, date: str) -> bool:
        raise NotImplementedError
