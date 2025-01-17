from dataclasses import dataclass

from src.domain.lift_pass_cost import LiftPassCost
from src.domain.lift_pass_cost_factory import LiftPassCostFactory
from src.domain.lift_pass_holiday_repository import LiftPassHolidayRepository
from src.domain.lift_pass_props import LiftPassProps
from src.domain.lift_pass_repository import LiftPassRepository


@dataclass
class GetPricesQuery:
    lift_pass_props: list[LiftPassProps]


class GetPricesQueryHandler:
    def __init__(
        self,
        pass_repository: LiftPassRepository,
        holiday_repository: LiftPassHolidayRepository,
    ) -> None:
        self.pass_repository = pass_repository
        self.holiday_repository = holiday_repository

    def execute(self, query: GetPricesQuery) -> list:
        prices = []
        for prop in query.lift_pass_props:
            lift_pass_cost = self._create_lift_pass_cost(prop)
            cost = lift_pass_cost.calculate()
            prices.append({"pass_type": prop.pass_type.value, "cost": cost})
        return prices

    def _create_lift_pass_cost(self, lift_pass_props: LiftPassProps) -> LiftPassCost:
        return LiftPassCostFactory.make(
            self.pass_repository,
            self.holiday_repository,
            lift_pass_props,
        )
