from expects import equal, expect

from src.infrastructure.mysql.sql_lift_pass_repository import (
    SqlLiftPassRepositoryFactory,
)


class TestSqlLiftPassRepositoryIntegration:
    def test_save_and_find_lift_pass(self) -> None:
        repository = SqlLiftPassRepositoryFactory.make()
        pass_type = "night"
        base_price = 10

        repository.save(pass_type, base_price)
        lift_pass_base_price = repository.find_base_price(pass_type)

        expect(lift_pass_base_price).to(equal(base_price))

    def teardown_method(self) -> None:
        sql_lift_pass_repository = SqlLiftPassRepositoryFactory.make()
        sql_lift_pass_repository.delete("night")
