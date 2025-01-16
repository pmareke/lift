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
from src.use_cases.get_price_query_handler import GetPriceQuery, GetPriceQueryHandler


class TestGetPriceQueryHandler:
    def test_get_night_price(self) -> None:
        pass_type = LiftPassType.NIGHT
        base_price = 50
        lift_pass = LiftPass(pass_type, base_price)
        holiday_repository = Mimic(Spy, SqlLiftPassHolidayRepository)
        with Mimic(Stub, SqlLiftPassRepository) as lift_pass_repository:
            lift_pass_repository.find_by(pass_type).returns(lift_pass)
        price = LiftPassPrice(pass_type, age="20", date="2021-12-25")
        query = GetPriceQuery(price)
        handler = GetPriceQueryHandler(lift_pass_repository, holiday_repository)

        cost = handler.execute(query)

        expect(cost).to(equal(base_price))
        expect(holiday_repository.is_holiday).not_to(have_been_called_with("2021-12-25"))

    def test_get_one_jour_price(self) -> None:
        pass_type = LiftPassType.ONE_JOUR
        base_price = 50
        lift_pass = LiftPass(pass_type, base_price)
        with Mimic(Stub, SqlLiftPassRepository) as lift_pass_repository:
            lift_pass_repository.find_by(pass_type).returns(lift_pass)
        with Mimic(Stub, SqlLiftPassHolidayRepository) as holiday_repository:
            holiday_repository.is_holiday("2021-12-25").returns(True)
        price = LiftPassPrice(pass_type, age="20", date="2021-12-25")
        query = GetPriceQuery(price)
        handler = GetPriceQueryHandler(lift_pass_repository, holiday_repository)

        cost = handler.execute(query)

        expect(cost).to(equal(base_price))
