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
    def test_get_prices(self) -> None:
        pass_type = LiftPassType.NIGHT
        base_price = 50
        lift_pass = LiftPass(pass_type, base_price)
        holiday_repository = Mimic(Spy, SqlLiftPassHolidayRepository)
        with Mimic(Stub, SqlLiftPassRepository) as lift_pass_repository:
            lift_pass_repository.find_by(pass_type).returns(lift_pass)
        price = LiftPassPrice(pass_type, age="20", date="2021-12-25")
        query = GetPricesQuery([price])
        handler = GetPricesQueryHandler(lift_pass_repository, holiday_repository)

        prices = handler.execute(query)

        expect(prices).to(equal([{"pass_type": pass_type.value, "cost": 50}]))
