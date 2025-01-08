from doublex import ANY_ARG, Mimic, Spy, Stub
from doublex_expects import have_been_called_with
from expects import equal, expect

from src.infrastructure.mysql.sql_lift_pass_holiday_repository import (
    SqlLiftPassHolidayRepository,
)
from src.infrastructure.mysql.sql_lift_pass_repository import SqlLiftPassRepository
from src.use_cases.get_price_query_handler import GetPriceQuery, GetPriceQueryHandler


class TestGetPriceQueryHandler:
    def test_get_night(self) -> None:
        holiday_repository = Mimic(Spy, SqlLiftPassHolidayRepository)
        with Mimic(Stub, SqlLiftPassRepository) as lift_pass_repository:
            lift_pass_repository.find_base_price("night").returns(50)
        query = GetPriceQuery("night", age="20", date="2021-12-25")
        handler = GetPriceQueryHandler(lift_pass_repository, holiday_repository)

        cost = handler.execute(query)

        expect(cost).to(equal(50))
        expect(holiday_repository.is_holiday).not_to(have_been_called_with("2021-12-25"))

    def test_get_one_jour(self) -> None:
        with Mimic(Stub, SqlLiftPassRepository) as lift_pass_repository:
            lift_pass_repository.find_base_price("1jour").returns(50)
        with Mimic(Stub, SqlLiftPassHolidayRepository) as holiday_repository:
            holiday_repository.is_holiday("2021-12-25").returns(True)
        query = GetPriceQuery("1jour", age="20", date="2021-12-25")
        handler = GetPriceQueryHandler(lift_pass_repository, holiday_repository)

        cost = handler.execute(query)

        expect(cost).to(equal(50))
