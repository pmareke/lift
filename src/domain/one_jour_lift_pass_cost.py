import math
from datetime import datetime

from src.domain.lift_pass_cost import LiftPassCost
from src.domain.lift_pass_holiday_repository import LiftPassHolidayRepository
from src.domain.lift_pass_repository import LiftPassRepository
from src.domain.lift_pass_type import LiftPassType


class OneJourLiftPassCost(LiftPassCost):
    def __init__(
        self,
        pass_repository: LiftPassRepository,
        holiday_repository: LiftPassHolidayRepository,
        age: str | None = None,
        date: str | None = None,
    ) -> None:
        self.pass_repository = pass_repository
        self.holiday_repository = holiday_repository
        self.age = age
        self.date = date

    def calculate(self) -> float:
        lift_pass = self.pass_repository.find_by(LiftPassType.ONE_JOUR)
        base_price = lift_pass.base_price

        # Base reduction for everyone based on the date
        percentage_to_pay = self._calculate_percentage_to_pay(self.date)
        cost = math.ceil(base_price * percentage_to_pay)

        # No extra discount without age
        if not self.age:
            return cost

        age_value = int(self.age)
        # Zero cost for kids under 6
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
        # 35% discount on Mondays if it's not a holiday
        if self._is_monday(date) and not is_holiday:
            return 0.65

        # No discount
        return 1

    def _is_monday(self, date: str) -> bool:
        iso_date = datetime.fromisoformat(date)
        return iso_date.weekday() == 0  # MONDAY
