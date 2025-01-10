from expects import equal, expect

from src.domain.lift_pass import LiftPass
from src.domain.lift_pass_type import LiftPassType
from src.infrastructure.mysql.sql_lift_pass_repository import (
    SqlLiftPassRepositoryFactory,
)


class TestSqlLiftPassRepositoryIntegration:
    def test_save_and_find_lift_pass(self) -> None:
        repository = SqlLiftPassRepositoryFactory.make()
        pass_type = LiftPassType.NIGHT
        base_price = 10
        lift_pass = LiftPass(pass_type, base_price)

        repository.save(lift_pass)
        found_lift_pass = repository.find_by(pass_type)

        expect(found_lift_pass).to(equal(lift_pass))

    def teardown_method(self) -> None:
        sql_lift_pass_repository = SqlLiftPassRepositoryFactory.make()
        sql_lift_pass_repository.delete(LiftPassType.NIGHT)
