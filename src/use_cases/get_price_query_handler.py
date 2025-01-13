import math
from dataclasses import dataclass
from datetime import datetime

from src.domain.lift_pass_holiday_repository import LiftPassHolidayRepository
from src.domain.lift_pass_repository import LiftPassRepository
from src.domain.lift_pass_type import LiftPassType


@dataclass
class GetPriceQuery:
    pass_type: LiftPassType
    age: str | None = None
    date: str | None = None


class GetPriceQueryHandler:
    def __init__(
        self,
        pass_repository: LiftPassRepository,
        holiday_repository: LiftPassHolidayRepository,
    ) -> None:
        self.pass_repository = pass_repository
        self.holiday_repository = holiday_repository

    def execute(self, query: GetPriceQuery) -> float:
        pass_type = query.pass_type
        age = query.age
        date = query.date

        if pass_type.is_night:
            return self._night_lift_pass_cost(age)

        return self._one_jour_lift_pass_cost(age, date)

    def _night_lift_pass_cost(self, age: str | None) -> float:
        # Free cost without age
        if not age:
            return 0

        age_value = int(age)
        # Free cost for kids
        if age_value < 6:
            return 0

        lift_pass = self.pass_repository.find_by(LiftPassType.NIGHT)
        base_price = lift_pass.base_price

        # No discount for adults under 65
        if age_value <= 64:
            return base_price

        # 60% discount for seniors over 65
        return math.ceil(base_price * 0.4)

    def _one_jour_lift_pass_cost(self, age: str | None, date: str | None) -> float:
        lift_pass = self.pass_repository.find_by(LiftPassType.ONE_JOUR)
        base_price = lift_pass.base_price

        # Base reduction for everyone based on the date
        percentage_to_pay = self._calculate_percentage_to_pay(date)
        cost = math.ceil(base_price * percentage_to_pay)

        # No extra discount without age
        if not age:
            return cost

        age_value = int(age)
        # Free cost for kids under 6
        if age_value < 6:
            return 0

        # Extra 30% reduction for children above 6 and under 15
        if age_value < 15:
            return math.ceil(base_price * 0.7)

        # No extra reduction for adults above 15 and under 65
        if age_value <= 64:
            return cost

        # Extra 25% reduction for seniors
        return math.ceil(cost * 0.75)

    def _calculate_percentage_to_pay(self, date: str | None) -> float:
        # No discount without date
        if not date:
            return 1

        is_holiday = self.holiday_repository.is_holiday(date)
        # 35% reduction on Mondays if it's not a holiday
        if self._is_monday(date) and not is_holiday:
            return 0.65

        # No reduction
        return 1

    def _is_monday(self, date: str) -> bool:
        iso_date = datetime.fromisoformat(date)
        return iso_date.weekday() == 0  # MONDAY
