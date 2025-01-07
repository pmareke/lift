from expects import expect, be_false, be_true

from src.infrastructure.mysql.sql_lift_holiday_repository import (
    SqlLiftHolidayRepositoryFactory,
)


class TestSqlLiftHolidayRepositoryIntegration:
    def test_is_holiday(self) -> None:
        holiday_repository = SqlLiftHolidayRepositoryFactory.make()

        is_holiday = holiday_repository.is_holiday("2019-02-18")

        expect(is_holiday).to(be_true)

    def test_is_not_holiday(self) -> None:
        holiday_repository = SqlLiftHolidayRepositoryFactory.make()

        is_holiday = holiday_repository.is_holiday("2021-01-01")

        expect(is_holiday).to(be_false)
