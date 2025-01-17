from src.domain.lift_pass_cost import LiftPassCost
from src.domain.lift_pass_holiday_repository import LiftPassHolidayRepository
from src.domain.lift_pass_price import LiftPassPrice
from src.domain.lift_pass_repository import LiftPassRepository
from src.domain.night_lift_pass_cost import NightLiftPassCost
from src.domain.one_jour_lift_pass_cost import OneJourLiftPassCost


class LiftPassCostFactory:
    @staticmethod
    def make(
        pass_repository: LiftPassRepository,
        holiday_repository: LiftPassHolidayRepository,
        price: LiftPassPrice,
    ) -> LiftPassCost:
        pass_type = price.pass_type
        age = price.age
        date = price.date
        if pass_type.is_night:
            return NightLiftPassCost(pass_repository, age)

        return OneJourLiftPassCost(pass_repository, holiday_repository, age, date)
