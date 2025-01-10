from dataclasses import dataclass

from src.domain.lift_pass_type import LiftPassType


@dataclass
class LiftPass:
    pass_type: LiftPassType
    base_price: float
