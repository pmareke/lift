import math

from dataclasses import dataclass
from datetime import datetime

from src.infrastructure.mysql.sql_lift_holiday_repository import SqlLiftHolidayRepository
from src.infrastructure.mysql.sql_lift_price_repository import SqlLiftPriceRepository


@dataclass
class GetPriceQuery:
    liff_pass_type: str
    age: str | None = None
    date: str | None = None


class GetPriceQueryHandler:
    def __init__(
        self,
        lift_price_repository: SqlLiftPriceRepository,
        lift_holiday_repository: SqlLiftHolidayRepository,
    ) -> None:
        self.lift_price_repository = lift_price_repository
        self.lift_holiday_repository = lift_holiday_repository

    def execute(self, query: GetPriceQuery) -> float:
        pass_type = query.liff_pass_type
        age = query.age
        date = query.date

        if pass_type == "night":
            return self._night_cost(age)
        return self._jour_cost(age, date)

    def _night_cost(self, age: str | None) -> float:
        cost = self.lift_price_repository.get_by_type("night")

        if not age:
            return 0

        age_value = int(age)
        if age_value < 6:
            # Free for kids
            return 0

        if age_value <= 64:
            return cost

        # Extra reduction for seniors
        return math.ceil(cost * 0.4)

    def _jour_cost(self, age: str | None, date: str | None) -> float:
        cost = self.lift_price_repository.get_by_type("1jour")
        calculated_cost = self._calculate_cost(date, cost)

        # TODO: apply reduction for others
        if not age:
            return calculated_cost

        age_value = int(age)
        if age_value < 6:
            # Free for kids
            return 0

        if age_value < 15:
            # Extra reduction for children
            return math.ceil(cost * 0.7)

        if age_value <= 64:
            return calculated_cost

        # Extra reduction for seniors
        return math.ceil(calculated_cost * 0.75)

    def _calculate_cost(self, date: str | None, cost: float) -> float:
        if not date:
            return cost

        is_holiday = self.lift_holiday_repository.is_holiday(date)
        if self._is_monday(date) and not is_holiday:
            return math.ceil(0.65 * cost)
        return cost

    def _is_monday(self, date: str) -> bool:
        iso_date = datetime.fromisoformat(date)
        return iso_date.weekday() == 0
