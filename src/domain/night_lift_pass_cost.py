import math

from src.domain.lift_pass_cost import LiftPassCost
from src.domain.lift_pass_repository import LiftPassRepository
from src.domain.lift_pass_type import LiftPassType


class NightLiftPassCost(LiftPassCost):
    def __init__(
        self,
        pass_repository: LiftPassRepository,
        age: str | None = None,
    ) -> None:
        self.pass_repository = pass_repository
        self.age = age

    def calculate(self) -> float:
        # Zero cost without age
        if not self.age:
            return 0

        age_value = int(self.age)
        # Zero cost for kids
        if age_value < 6:
            return 0

        lift_pass = self.pass_repository.find_by(LiftPassType.NIGHT)
        base_price = lift_pass.base_price

        # No discount for adults under 65
        if age_value <= 64:
            return base_price

        # 60% discount for seniors over 65
        return math.ceil(base_price * 0.4)
