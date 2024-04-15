from expects import expect, equal
from src.db import create_lift_pass_db_connection
from src.infrastructure.mysql.sql_lift_price_repository import (
    SqlLiftPriceRepositoryFactory,
)


class TestSqlLiftPriceRepositoryIntegration:
    def test_add_and_get_price(self) -> None:
        sql_lift_price_repository = SqlLiftPriceRepositoryFactory.make()
        lift_pass_type = "day"
        cost = 51

        sql_lift_price_repository.save(lift_pass_type, cost)
        expected_cost = sql_lift_price_repository.get_by_type(lift_pass_type)

        expect(expected_cost).to(equal(cost))
