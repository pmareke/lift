from pymysql.cursors import Cursor

from src.infrastructure.mysql.connection.create_connection import create_connection


class SqlLiftPassRepository:
    TABLE_NAME = "base_price"

    def __init__(self, cursor: Cursor) -> None:
        self.cursor = cursor

    def save(self, lift_pass_type: str, cost: float) -> None:
        statement = f"INSERT INTO {self.TABLE_NAME} (type, cost) VALUES (?, ?) ON DUPLICATE KEY UPDATE cost = ?"
        self.cursor.execute(statement, [lift_pass_type, cost, cost])

    def delete(self, pass_lift_type: str) -> None:
        statement = f"DELETE FROM {self.TABLE_NAME} WHERE type = ? "
        self.cursor.execute(statement, pass_lift_type)

    def find_base_price(self, lift_pass_type: str) -> float:
        statement = f"SELECT cost FROM {self.TABLE_NAME} WHERE type = ? "
        self.cursor.execute(statement, [lift_pass_type])
        result = self.cursor.fetchone()
        if not result:
            raise Exception(f"Base price for {lift_pass_type} not found")
        return float(result[0])


class SqlLiftPassRepositoryFactory:
    @staticmethod
    def make() -> SqlLiftPassRepository:
        connection = create_connection()
        cursor = connection.cursor()
        return SqlLiftPassRepository(cursor)
