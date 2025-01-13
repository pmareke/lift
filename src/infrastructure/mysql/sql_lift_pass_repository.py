from pymysql.cursors import Cursor

from src.domain.exceptions import LiftPassTypeNotFoundException
from src.domain.lift_pass import LiftPass
from src.domain.lift_pass_repository import LiftPassRepository
from src.domain.lift_pass_type import LiftPassType
from src.infrastructure.mysql.connection.create_connection import create_connection


class SqlLiftPassRepository(LiftPassRepository):
    TABLE_NAME = "base_price"

    def __init__(self, cursor: Cursor) -> None:
        self.cursor = cursor

    def save(self, lift_pass: LiftPass) -> None:
        pass_type = lift_pass.pass_type.value
        base_price = lift_pass.base_price
        statement = f"INSERT INTO {self.TABLE_NAME} (type, cost) VALUES (?, ?) ON DUPLICATE KEY UPDATE cost = ?"
        self.cursor.execute(statement, [pass_type, base_price, base_price])

    def delete(self, pass_type: LiftPassType) -> None:
        statement = f"DELETE FROM {self.TABLE_NAME} WHERE type = ? "
        self.cursor.execute(statement, pass_type.value)

    def find_by(self, pass_type: LiftPassType) -> LiftPass:
        statement = f"SELECT cost FROM {self.TABLE_NAME} WHERE type = ? "
        self.cursor.execute(statement, [pass_type.value])
        result = self.cursor.fetchone()
        if not result:
            raise LiftPassTypeNotFoundException(f"Base price for {pass_type} not found")
        return LiftPass(pass_type, float(result[0]))


class SqlLiftPassRepositoryFactory:
    @staticmethod
    def make() -> SqlLiftPassRepository:
        connection = create_connection()
        cursor = connection.cursor()
        return SqlLiftPassRepository(cursor)
