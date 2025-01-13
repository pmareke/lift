import math
from dataclasses import dataclass
from datetime import datetime

from src.domain.lift_pass_type import LiftPassType
from src.infrastructure.mysql.sql_lift_pass_holiday_repository import (
    SqlLiftPassHolidayRepository,
)
from src.infrastructure.mysql.sql_lift_pass_repository import SqlLiftPassRepository


@dataclass
class GetPriceQuery:
    pass_type: LiftPassType
    age: str | None = None
    date: str | None = None


class GetPriceQueryHandler:
    def __init__(
        self,
        lift_pass_repository: SqlLiftPassRepository,
        lift_pass_holiday_repository: SqlLiftPassHolidayRepository,
    ) -> None:
        self.lift_pass_repository = lift_pass_repository
        self.lift_pass_holiday_repository = lift_pass_holiday_repository

    def execute(self, query: GetPriceQuery) -> float:
        pass_type = query.pass_type
        age = query.age
        date = query.date

        if pass_type.is_night:
            return self._night_lift_pass_cost(age)

        return self._one_jour_lift_pass_cost(age, date)

    def _night_lift_pass_cost(self, age: str | None) -> float:
        # Free without age
        if not age:
            return 0

        age_value = int(age)
        # Free for kids
        if age_value < 6:
            return 0

        lift_pass = self.lift_pass_repository.find_by(LiftPassType.NIGHT)

        # Without discount for adults under 65
        if age_value <= 64:
            return lift_pass.base_price

        # Extra 60% reduction for seniors above 65
        return math.ceil(lift_pass.base_price * 0.4)

    def _one_jour_lift_pass_cost(self, age: str | None, date: str | None) -> float:
        lift_pass = self.lift_pass_repository.find_by(LiftPassType.ONE_JOUR)

        # Base reduction for everyone based on the date
        percentage_to_pay = self._calculate_percentage_to_pay(date)
        cost = math.ceil(lift_pass.base_price * percentage_to_pay)

        # No extra reduction without age
        if not age:
            return cost

        age_value = int(age)
        # Free for kids under 6
        if age_value < 6:
            return 0

        # Extra 30% reduction for children above 6 and under 15
        if age_value < 15:
            return math.ceil(lift_pass.base_price * 0.7)  # 70% - 30% reduction

        # No extra reduction for adults above 15 and under 65
        if age_value <= 64:
            return cost

        # Extra 25% reduction for seniors
        return math.ceil(cost * 0.75)  # 75% - 25% reduction

    def _calculate_percentage_to_pay(self, date: str | None) -> float:
        if not date:
            return 1  # 100% - No reduction

        is_holiday = self.lift_pass_holiday_repository.is_holiday(date)
        if self._is_monday(date) and not is_holiday:
            return 0.65  # 65% - 35% reduction

        return 1  # 100% - No reduction

    def _is_monday(self, date: str) -> bool:
        iso_date = datetime.fromisoformat(date)
        return iso_date.weekday() == 0  # MONDAY
