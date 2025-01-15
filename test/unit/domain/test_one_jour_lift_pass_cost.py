from doublex import ANY_ARG, Mimic, Stub
from expects import equal, expect

from src.domain.lift_pass import LiftPass
from src.domain.lift_pass_type import LiftPassType
from src.domain.one_jour_lift_pass_cost import OneJourLiftPassCost
from src.infrastructure.mysql.sql_lift_pass_holiday_repository import (
    SqlLiftPassHolidayRepository,
)
from src.infrastructure.mysql.sql_lift_pass_repository import SqlLiftPassRepository


class TestOneJourLiftPassCost:
    def test_without_date(self) -> None:
        base_price = 100
        lift_pass = LiftPass(LiftPassType.ONE_JOUR, base_price)
        with Mimic(Stub, SqlLiftPassRepository) as pass_repository:
            pass_repository.find_by(LiftPassType.ONE_JOUR).returns(lift_pass)
        holiday_repository = Stub()
        one_jour_pass = OneJourLiftPassCost(
            pass_repository,
            holiday_repository,
            age="50",
        )

        cost = one_jour_pass.calculate()

        expect(cost).to(equal(base_price))

    def test_not_holiday_but_monday_has_35_discount(self) -> None:
        base_price = 100
        lift_pass = LiftPass(LiftPassType.ONE_JOUR, base_price)
        with Mimic(Stub, SqlLiftPassRepository) as pass_repository:
            pass_repository.find_by(LiftPassType.ONE_JOUR).returns(lift_pass)
        with Mimic(Stub, SqlLiftPassHolidayRepository) as holiday_repository:
            holiday_repository.is_holiday(ANY_ARG).returns(False)
        one_jour_pass = OneJourLiftPassCost(
            pass_repository,
            holiday_repository,
            date="2021-08-02",
        )

        cost = one_jour_pass.calculate()

        expect(cost).to(equal(base_price * 0.65))

    def test_holiday_but_monday_does_not_have_discount(self) -> None:
        base_price = 100
        lift_pass = LiftPass(LiftPassType.ONE_JOUR, base_price)
        with Mimic(Stub, SqlLiftPassRepository) as pass_repository:
            pass_repository.find_by(LiftPassType.ONE_JOUR).returns(lift_pass)
        with Mimic(Stub, SqlLiftPassHolidayRepository) as holiday_repository:
            holiday_repository.is_holiday(ANY_ARG).returns(True)
        one_jour_pass = OneJourLiftPassCost(
            pass_repository,
            holiday_repository,
            date="2021-08-02",
        )

        cost = one_jour_pass.calculate()

        expect(cost).to(equal(base_price))

    def test_holiday_but_not_monday_does_not_have_discount(self) -> None:
        base_price = 100
        lift_pass = LiftPass(LiftPassType.ONE_JOUR, base_price)
        with Mimic(Stub, SqlLiftPassRepository) as pass_repository:
            pass_repository.find_by(LiftPassType.ONE_JOUR).returns(lift_pass)
        with Mimic(Stub, SqlLiftPassHolidayRepository) as holiday_repository:
            holiday_repository.is_holiday(ANY_ARG).returns(True)
        one_jour_pass = OneJourLiftPassCost(
            pass_repository,
            holiday_repository,
            date="2021-08-03",
        )

        cost = one_jour_pass.calculate()

        expect(cost).to(equal(base_price))

    def test_not_holiday_and_not_monday_does_not_have_discount(self) -> None:
        base_price = 100
        lift_pass = LiftPass(LiftPassType.ONE_JOUR, base_price)
        with Mimic(Stub, SqlLiftPassRepository) as pass_repository:
            pass_repository.find_by(LiftPassType.ONE_JOUR).returns(lift_pass)
        with Mimic(Stub, SqlLiftPassHolidayRepository) as holiday_repository:
            holiday_repository.is_holiday(ANY_ARG).returns(False)
        one_jour_pass = OneJourLiftPassCost(
            pass_repository,
            holiday_repository,
            date="2021-08-03",
        )

        cost = one_jour_pass.calculate()

        expect(cost).to(equal(base_price))

    def test_without_age(self) -> None:
        base_price = 100
        lift_pass = LiftPass(LiftPassType.ONE_JOUR, base_price)
        with Mimic(Stub, SqlLiftPassRepository) as pass_repository:
            pass_repository.find_by(LiftPassType.ONE_JOUR).returns(lift_pass)
        holiday_repository = Stub()
        one_jour_pass = OneJourLiftPassCost(pass_repository, holiday_repository, date="2021-08-03")

        cost = one_jour_pass.calculate()

        expect(cost).to(equal(base_price))

    def test_under_6_is_free(self) -> None:
        base_price = 100
        lift_pass = LiftPass(LiftPassType.ONE_JOUR, base_price)
        with Mimic(Stub, SqlLiftPassRepository) as pass_repository:
            pass_repository.find_by(LiftPassType.ONE_JOUR).returns(lift_pass)
        holiday_repository = Stub()
        one_jour_pass = OneJourLiftPassCost(
            pass_repository,
            holiday_repository,
            age="5",
        )

        cost = one_jour_pass.calculate()

        expect(cost).to(equal(0))

    def test_over_5_and_under_15_has_30_discount(self) -> None:
        base_price = 100
        lift_pass = LiftPass(LiftPassType.ONE_JOUR, base_price)
        with Mimic(Stub, SqlLiftPassRepository) as pass_repository:
            pass_repository.find_by(LiftPassType.ONE_JOUR).returns(lift_pass)
        holiday_repository = Stub()
        one_jour_pass = OneJourLiftPassCost(
            pass_repository,
            holiday_repository,
            age="14",
        )

        cost = one_jour_pass.calculate()

        expect(cost).to(equal(base_price * 0.7))

    def test_over_14_and_under_65_does_not_have_discount(self) -> None:
        base_price = 100
        lift_pass = LiftPass(LiftPassType.ONE_JOUR, base_price)
        with Mimic(Stub, SqlLiftPassRepository) as pass_repository:
            pass_repository.find_by(LiftPassType.ONE_JOUR).returns(lift_pass)
        holiday_repository = Stub()
        one_jour_pass = OneJourLiftPassCost(
            pass_repository,
            holiday_repository,
            age="50",
        )

        cost = one_jour_pass.calculate()

        expect(cost).to(equal(base_price))

    def test_over_64_has_25_discount(self) -> None:
        base_price = 100
        lift_pass = LiftPass(LiftPassType.ONE_JOUR, base_price)
        with Mimic(Stub, SqlLiftPassRepository) as pass_repository:
            pass_repository.find_by(LiftPassType.ONE_JOUR).returns(lift_pass)
        holiday_repository = Stub()
        one_jour_pass = OneJourLiftPassCost(
            pass_repository,
            holiday_repository,
            age="70",
        )

        cost = one_jour_pass.calculate()

        expect(cost).to(equal(base_price * 0.75))
