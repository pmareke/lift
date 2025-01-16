from doublex import Mimic, Spy, Stub
from doublex_expects import have_been_called_with
from expects import equal, expect

from src.domain.lift_pass import LiftPass
from src.domain.lift_pass_price import LiftPassPrice
from src.domain.lift_pass_type import LiftPassType
from src.infrastructure.mysql.sql_lift_pass_holiday_repository import (
    SqlLiftPassHolidayRepository,
)
from src.infrastructure.mysql.sql_lift_pass_repository import SqlLiftPassRepository
from src.use_cases.get_prices_query_handler import GetPricesQuery, GetPricesQueryHandler


class TestGetPricesQueryHandler:
    def test_get_night_and_one_jour_prices(self) -> None:
        night_pass_type = LiftPassType.NIGHT
        base_price = 50
        night_lift_pass = LiftPass(night_pass_type, base_price)
        one_jour_pass_type = LiftPassType.ONE_JOUR
        base_price = 50
        one_jour_lift_pass = LiftPass(one_jour_pass_type, base_price)
        holiday_repository = Mimic(Spy, SqlLiftPassHolidayRepository)
        with Mimic(Stub, SqlLiftPassRepository) as lift_pass_repository:
            lift_pass_repository.find_by(night_pass_type).returns(night_lift_pass)
            lift_pass_repository.find_by(one_jour_pass_type).returns(one_jour_lift_pass)
        night_price = LiftPassPrice(night_pass_type, age="20", date="2021-12-25")
        one_jour_price = LiftPassPrice(one_jour_pass_type, age="20", date="2021-12-25")
        query = GetPricesQuery([night_price, one_jour_price])
        handler = GetPricesQueryHandler(lift_pass_repository, holiday_repository)

        prices = handler.execute(query)

        expect(prices).to(
            equal(
                [
                    {"pass_type": night_pass_type.value, "cost": 50},
                    {"pass_type": one_jour_pass_type.value, "cost": 50},
                ]
            )
        )
