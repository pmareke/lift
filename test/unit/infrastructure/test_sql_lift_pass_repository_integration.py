from doublex import Mimic, Stub
from expects import expect, raise_error
from pymysql.cursors import Cursor

from src.infrastructure.mysql.sql_lift_pass_repository import SqlLiftPassRepository


class TestSqlLiftPassRepository:
    def test_save_and_find_lift_pass(self) -> None:
        pass_type = "day"
        with Mimic(Stub, Cursor) as cursor:
            cursor.fetchone().returns(None)
        sql_lift_pass_repository = SqlLiftPassRepository(cursor)

        error_message = f"Base price for {pass_type} not found"
        expect(lambda: sql_lift_pass_repository.find_base_price(pass_type)).to(raise_error(Exception, error_message))
