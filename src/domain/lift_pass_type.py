from enum import Enum


class LiftPassType(Enum):
    NIGHT = "night"
    ONE_JOUR = "1jour"

    @property
    def is_night(self) -> bool:
        return self == LiftPassType.NIGHT
