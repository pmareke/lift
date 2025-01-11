import math
from datetime import datetime

from src.domain.lift_pass_cost import LiftPassCost
from src.domain.lift_pass_type import LiftPassType


class OneJourLiftPassCost(LiftPassCost):
    PASS_TYPE = LiftPassType.ONE_JOUR

    def __init__(self, pass_repository, holiday_repository, age: str | None, date: str | None):
        self.pass_repository = pass_repository
        self.holiday_repository = holiday_repository
        self.age = age
        self.date = date

    def cost(self) -> float:
        lift_pass = self.pass_repository.find_by(self.PASS_TYPE)
        percentage_to_pay = self._calculate_percentage_to_pay(self.date)
        cost = math.ceil(lift_pass.base_price * percentage_to_pay)

        # TODO: apply reduction for others
        if not self.age:
            return cost

        age_value = int(self.age)
        if age_value < 6:
            # Free for kids
            return 0

        if age_value < 15:
            # Extra reduction for children
            return math.ceil(lift_pass.base_price * 0.7)  # 70% - 30% reduction

        if age_value <= 64:
            return cost

        # Extra reduction for seniors
        return math.ceil(cost * 0.75)  # 75% - 25% reduction

    def _calculate_percentage_to_pay(self, date: str | None) -> float:
        if not date:
            return 1  # 100% - No reduction

        is_holiday = self.holiday_repository.is_holiday(date)
        if self._is_monday(date) and not is_holiday:
            return 0.65  # 65% - 35% reduction

        return 1  # 100% - No reduction

    def _is_monday(self, date: str) -> bool:
        iso_date = datetime.fromisoformat(date)
        return iso_date.weekday() == 0  # MONDAY
