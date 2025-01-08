from expects import equal, expect

from src.infrastructure.mysql.sql_lift_pass_repository import (
    SqlLiftPassRepositoryFactory,
)


class TestSqlLiftPassRepositoryIntegration:
    def test_save_and_find_lift_pass(self) -> None:
        sql_lift_pass_repository = SqlLiftPassRepositoryFactory.make()
        pass_type = "day"
        base_price = 51

        sql_lift_pass_repository.save(pass_type, base_price)

        expected_base_price = sql_lift_pass_repository.find_base_price(pass_type)

        expect(expected_base_price).to(equal(base_price))

        sql_lift_pass_repository.delete(pass_type)
