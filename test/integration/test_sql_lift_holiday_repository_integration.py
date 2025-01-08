from expects import be_false, be_true, expect

from src.infrastructure.mysql.sql_lift_pass_holiday_repository import (
    SqlLiftPassHolidayRepositoryFactory,
)


class TestSqlLiftHolidayRepositoryIntegration:
    def test_is_holiday(self) -> None:
        holiday_repository = SqlLiftPassHolidayRepositoryFactory.make()

        is_holiday = holiday_repository.is_holiday("2019-02-18")

        expect(is_holiday).to(be_true)

    def test_is_not_holiday(self) -> None:
        holiday_repository = SqlLiftPassHolidayRepositoryFactory.make()

        is_holiday = holiday_repository.is_holiday("2021-01-01")

        expect(is_holiday).to(be_false)
