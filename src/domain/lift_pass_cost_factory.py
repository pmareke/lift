from dataclasses import dataclass

from src.domain.lift_pass_cost import LiftPassCost
from src.domain.lift_pass_type import LiftPassType
from src.domain.night_lift_pass_cost import NightLiftPassCost
from src.domain.one_jour_lift_pass_cost import OneJourLiftPassCost
from src.infrastructure.mysql.sql_lift_pass_holiday_repository import (
    SqlLiftPassHolidayRepository,
)
from src.infrastructure.mysql.sql_lift_pass_repository import SqlLiftPassRepository


@dataclass
class LiftPassCostProps:
    pass_type: LiftPassType
    age: str | None = None
    date: str | None = None


class LiftPassCostFactory:
    @staticmethod
    def make(
        lift_pass_cost_props: LiftPassCostProps,
        pass_repository: SqlLiftPassRepository,
        holiday_repository: SqlLiftPassHolidayRepository,
    ) -> LiftPassCost:
        pass_type = lift_pass_cost_props.pass_type
        age = lift_pass_cost_props.age
        date = lift_pass_cost_props.date

        if pass_type == LiftPassType.NIGHT:
            return NightLiftPassCost(pass_repository, age)

        return OneJourLiftPassCost(pass_repository, holiday_repository, age, date)
