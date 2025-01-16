from dataclasses import dataclass

from src.domain.lift_pass_type import LiftPassType


@dataclass
class LiftPassPrice:
    pass_type: LiftPassType
    age: str | None
    date: str | None
