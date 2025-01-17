from dataclasses import dataclass

from src.domain.lift_pass_cost import LiftPassCost
from src.domain.lift_pass_cost_factory import LiftPassCostFactory
from src.domain.lift_pass_holiday_repository import LiftPassHolidayRepository
from src.domain.lift_pass_props import LiftPassProps
from src.domain.lift_pass_repository import LiftPassRepository


@dataclass
class GetPriceQuery:
    props: LiftPassProps


class GetPriceQueryHandler:
    def __init__(
        self,
        pass_repository: LiftPassRepository,
        holiday_repository: LiftPassHolidayRepository,
    ) -> None:
        self.pass_repository = pass_repository
        self.holiday_repository = holiday_repository

    def execute(self, query: GetPriceQuery) -> float:
        lift_pass_cost = self._create_lift_pass_cost(query.props)
        return lift_pass_cost.calculate()

    def _create_lift_pass_cost(self, props: LiftPassProps) -> LiftPassCost:
        return LiftPassCostFactory.make(
            self.pass_repository,
            self.holiday_repository,
            props,
        )
