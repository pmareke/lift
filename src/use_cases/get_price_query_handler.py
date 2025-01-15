from dataclasses import dataclass

from src.domain.lift_pass_cost import LiftPassCost
from src.domain.lift_pass_cost_factory import LiftPassCostFactory, LiftPassCostProps
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
        lift_pass_cost = self._generate_lift_pass_cost(query)
        return lift_pass_cost.calculate()

    def _generate_lift_pass_cost(self, query: GetPriceQuery) -> LiftPassCost:
        pass_type = query.pass_type
        age = query.age
        date = query.date
        props = LiftPassCostProps(pass_type, age, date)
        return LiftPassCostFactory.make(
            props,
            self.pass_repository,
            self.holiday_repository,
        )
