from src.domain.lift_pass_cost import LiftPassCost
from src.domain.lift_pass_holiday_repository import LiftPassHolidayRepository
from src.domain.lift_pass_props import LiftPassProps
from src.domain.lift_pass_repository import LiftPassRepository
from src.domain.night_lift_pass_cost import NightLiftPassCost
from src.domain.one_jour_lift_pass_cost import OneJourLiftPassCost


class LiftPassCostFactory:
    @staticmethod
    def make(
        pass_repository: LiftPassRepository,
        holiday_repository: LiftPassHolidayRepository,
        lift_pass_props: LiftPassProps,
    ) -> LiftPassCost:
        pass_type = lift_pass_props.pass_type
        age = lift_pass_props.age
        date = lift_pass_props.date
        if pass_type.is_night:
            return NightLiftPassCost(pass_repository, age)

        return OneJourLiftPassCost(pass_repository, holiday_repository, age, date)
