import math

from src.domain.lift_pass_cost import LiftPassCost
from src.domain.lift_pass_type import LiftPassType
from src.infrastructure.mysql.sql_lift_pass_repository import SqlLiftPassRepository


class NightLiftPassCost(LiftPassCost):
    PASS_TYPE = LiftPassType.NIGHT

    def __init__(
        self, lift_pass_repository: SqlLiftPassRepository, age: str | None
    ) -> None:
        self.lift_pass_repository = lift_pass_repository
        self.age = age

    def cost(self) -> float:
        if not self.age:
            return 0

        age_value = int(self.age)
        if age_value < 6:
            # Free for kids
            return 0

        lift_pass = self.lift_pass_repository.find_by(self.PASS_TYPE)

        if age_value <= 64:
            return lift_pass.base_price

        # Extra reduction for seniors
        return math.ceil(lift_pass.base_price * 0.4)
