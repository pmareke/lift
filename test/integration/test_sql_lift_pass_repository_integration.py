from expects import equal, expect

from src.infrastructure.mysql.sql_lift_pass_repository import (
    SqlLiftPassRepositoryFactory,
)


class TestSqlLiftPassRepositoryIntegration:
    def test_lift_pass(self) -> None:
        sql_lift_pass_repository = SqlLiftPassRepositoryFactory.make()
        lift_pass_type = "day"
        cost = 51

        sql_lift_pass_repository.save(lift_pass_type, cost)
        expected_cost = sql_lift_pass_repository.find_by_type(lift_pass_type)

        expect(expected_cost).to(equal(cost))

        sql_lift_pass_repository.delete(lift_pass_type)
