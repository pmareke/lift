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
        if pass_type == "night":
            age = query.age
            return self._night_cost(age)
        elif pass_type == "1jour":
            age = query.age
            date = query.date
            return self._jour_cost(age, date)
        else:
            return 0

    def _night_cost(self, age: str | None) -> float:
        if not age:
            return 0

        age_value = int(age)
        if age_value < 6:
            # Free for kids
            return 0

        night_cost = self.lift_price_repository.get_by_type("night")

        if age_value <= 64:
            return night_cost

        # Extra reduction for seniors
        return math.ceil(night_cost * 0.4)

    def _jour_cost(self, age: str | None, date: str | None) -> float:
        cost = self.lift_price_repository.get_by_type("1jour")
        percentage = self._calculate_percentage(date)
        jour_cost = math.ceil(cost * percentage)

        # TODO: apply reduction for others
        if not age:
            return jour_cost

        age_value = int(age)
        if age_value < 6:
            # Free for kids
            return 0

        if age_value < 15:
            # Extra reduction for children
            return math.ceil(cost * 0.7)

        if age_value <= 64:
            return jour_cost

        # Extra reduction for seniors
        return math.ceil(jour_cost * 0.75)

    def _calculate_percentage(self, date: str | None) -> float:
        if not date:
            return 1

        is_holiday = self.lift_holiday_repository.is_holiday(date)
        if self._is_monday(date) and not is_holiday:
            return 0.65
        return 1

    def _is_monday(self, date: str) -> bool:
        iso_date = datetime.fromisoformat(date)
        return iso_date.weekday() == 0
