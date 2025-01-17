from dataclasses import dataclass

from src.domain.lift_pass_type import LiftPassType


@dataclass
class LiftPassProps:
    pass_type: LiftPassType
    age: str | None = None
    date: str | None = None
