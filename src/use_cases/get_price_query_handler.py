from dataclasses import dataclass

from src.domain.lift_pass_cost import LiftPassCost
from src.domain.lift_pass_cost_factory import LiftPassCostFactory, LiftPassCostProps
from src.domain.lift_pass_type import LiftPassType
from src.domain.night_lift_pass_cost import NightLiftPassCost
from src.domain.one_jour_lift_pass_cost import OneJourLiftPassCost
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
        pass_repository: SqlLiftPassRepository,
        holiday_repository: SqlLiftPassHolidayRepository,
    ) -> None:
        self.pass_repository = pass_repository
        self.holiday_repository = holiday_repository

    def execute(self, query: GetPriceQuery) -> float:
        lift_pass_cost_props = LiftPassCostProps(
            pass_type=query.pass_type,
            age=query.age,
            date=query.date,
        )
        lift_pass_cost = self._create_lift_pass_cost(lift_pass_cost_props)
        return lift_pass_cost.cost()

    def _create_lift_pass_cost(self, lift_pass_cost_props: LiftPassCostProps) -> LiftPassCost:
        return LiftPassCostFactory.make(
            lift_pass_cost_props,
            self.pass_repository,
            self.holiday_repository,
        )
