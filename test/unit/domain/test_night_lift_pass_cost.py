from doublex import Mimic, Stub
from expects import equal, expect

from src.domain.lift_pass import LiftPass
from src.domain.lift_pass_type import LiftPassType
from src.domain.night_lift_pass_cost import NightLiftPassCost
from src.infrastructure.mysql.sql_lift_pass_repository import SqlLiftPassRepository


class TestNightLiftPassCost:
    def test_without_date(self) -> None:
        pass_repository = Stub()
        night_pass = NightLiftPassCost(pass_repository)

        cost = night_pass.calculate()

        expect(cost).to(equal(0))

    def test_under_6_is_free(self) -> None:
        pass_repository = Stub()
        night_pass = NightLiftPassCost(pass_repository, "5")

        cost = night_pass.calculate()

        expect(cost).to(equal(0))

    def test_under_65_does_not_have_discount(self) -> None:
        base_price = 100
        lift_pass = LiftPass(LiftPassType.NIGHT, base_price)
        with Mimic(Stub, SqlLiftPassRepository) as pass_repository:
            pass_repository.find_by(LiftPassType.NIGHT).returns(lift_pass)
        night_pass = NightLiftPassCost(pass_repository, "50")

        cost = night_pass.calculate()

        expect(cost).to(equal(base_price))

    def test_over_64_has_60_discount(self) -> None:
        base_price = 100
        lift_pass = LiftPass(LiftPassType.NIGHT, base_price)
        with Mimic(Stub, SqlLiftPassRepository) as pass_repository:
            pass_repository.find_by(LiftPassType.NIGHT).returns(lift_pass)
        night_pass = NightLiftPassCost(pass_repository, "70")

        cost = night_pass.calculate()

        expect(cost).to(equal(base_price * 0.4))
