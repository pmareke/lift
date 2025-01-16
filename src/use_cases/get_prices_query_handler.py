from dataclasses import dataclass

from src.domain.lift_pass_cost import LiftPassCost
from src.domain.lift_pass_cost_factory import LiftPassCostFactory, LiftPassCostProps
from src.domain.lift_pass_holiday_repository import LiftPassHolidayRepository
from src.domain.lift_pass_price import LiftPassPrice
from src.domain.lift_pass_repository import LiftPassRepository


@dataclass
class GetPricesQuery:
    prices: list[LiftPassPrice]


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
        for price in query.prices:
            lift_pass_cost = self._generate_lift_pass_cost(price)
            lift_pass_price = {
                "pass_type": price.pass_type.value,
                "cost": lift_pass_cost.calculate(),
            }
            prices.append(lift_pass_price)
        return prices

    def _generate_lift_pass_cost(self, price: LiftPassPrice) -> LiftPassCost:
        pass_type = price.pass_type
        age = price.age
        date = price.date
        props = LiftPassCostProps(pass_type, age, date)
        return LiftPassCostFactory.make(
            props,
            self.pass_repository,
            self.holiday_repository,
        )
