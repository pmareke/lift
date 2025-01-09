import math
from dataclasses import dataclass
from datetime import datetime

from src.infrastructure.mysql.sql_lift_pass_holiday_repository import (
    SqlLiftPassHolidayRepository,
)
from src.infrastructure.mysql.sql_lift_pass_repository import SqlLiftPassRepository


@dataclass
class GetPriceQuery:
    liff_pass_type: str
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
        pass_type = query.liff_pass_type

        if pass_type == "night":
            return self._night_cost(query)

        if pass_type == "1jour":
            return self._jour_cost(query)

        return 0  # Not existing pass type

    def _night_cost(self, query: GetPriceQuery) -> float:
        if not query.age:
            return 0

        age_value = int(query.age)
        if age_value < 6:
            # Free for kids
            return 0

        base_price = self.lift_pass_repository.find_base_price("night")

        if age_value <= 64:
            return base_price

        # Extra reduction for seniors
        cost = math.ceil(base_price * 0.4)
        return cost

    def _jour_cost(self, query: GetPriceQuery) -> float:
        base_price = self.lift_pass_repository.find_base_price("1jour")
        percentage_to_pay = self._calculate_percentage_to_pay(query.date)
        cost = math.ceil(base_price * percentage_to_pay)

        # TODO: apply reduction for others
        if not query.age:
            return cost

        age_value = int(query.age)
        if age_value < 6:
            # Free for kids
            return 0

        if age_value < 15:
            # Extra reduction for children
            return math.ceil(base_price * 0.7)

        if age_value <= 64:
            return cost

        # Extra reduction for seniors
        return math.ceil(cost * 0.75)

    def _calculate_percentage_to_pay(self, date: str | None) -> float:
        if not date:
            return 1  # 100%

        is_holiday = self.lift_pass_holiday_repository.is_holiday(date)
        if self._is_monday(date) and not is_holiday:
            return 0.65  # 65%
        return 1  # 100%

    def _is_monday(self, date: str) -> bool:
        iso_date = datetime.fromisoformat(date)
        return iso_date.weekday() == 0  # MONDAY
