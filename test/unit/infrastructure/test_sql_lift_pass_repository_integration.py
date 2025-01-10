from doublex import Mimic, Stub
from expects import expect, raise_error
from pymysql.cursors import Cursor

from src.domain.exceptions import LiftPassTypeNotFoundException
from src.domain.lift_pass_type import LiftPassType
from src.infrastructure.mysql.sql_lift_pass_repository import SqlLiftPassRepository


class TestSqlLiftPassRepository:
    def test_save_and_find_lift_pass(self) -> None:
        pass_type = LiftPassType.NIGHT
        with Mimic(Stub, Cursor) as cursor:
            cursor.fetchone().returns(None)
        sql_lift_pass_repository = SqlLiftPassRepository(cursor)

        error_message = f"Base price for {pass_type} not found"
        expect(lambda: sql_lift_pass_repository.find_by(pass_type)).to(
            raise_error(LiftPassTypeNotFoundException, error_message)
        )
