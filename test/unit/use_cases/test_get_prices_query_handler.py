from doublex import Mimic, Stub
from expects import equal, expect

from src.domain.lift_pass import LiftPass
from src.domain.lift_pass_props import LiftPassProps
from src.domain.lift_pass_type import LiftPassType
from src.infrastructure.mysql.sql_lift_pass_holiday_repository import (
    SqlLiftPassHolidayRepository,
)
from src.infrastructure.mysql.sql_lift_pass_repository import SqlLiftPassRepository
from src.use_cases.get_prices_query_handler import GetPricesQuery, GetPricesQueryHandler


class TestGetPricesQueryHandler:
    def test_get_multiple_prices(self) -> None:
        night_pass_type = LiftPassType.NIGHT
        base_price = 50
        night_lift_pass = LiftPass(night_pass_type, base_price)
        one_jour_pass_type = LiftPassType.ONE_JOUR
        one_jour_lift_pass = LiftPass(one_jour_pass_type, base_price)
        holiday_repository = Mimic(Stub, SqlLiftPassHolidayRepository)
        with Mimic(Stub, SqlLiftPassRepository) as lift_pass_repository:
            lift_pass_repository.find_by(night_pass_type).returns(night_lift_pass)
            lift_pass_repository.find_by(one_jour_pass_type).returns(one_jour_lift_pass)
        props = [
            LiftPassProps(night_pass_type),
            LiftPassProps(one_jour_pass_type),
        ]
        query = GetPricesQuery(props)
        handler = GetPricesQueryHandler(lift_pass_repository, holiday_repository)

        prices = handler.execute(query)

        expect(prices).to(
            equal(
                [
                    {"pass_type": night_pass_type.value, "cost": 0},
                    {"pass_type": one_jour_pass_type.value, "cost": base_price},
                ]
            )
        )
