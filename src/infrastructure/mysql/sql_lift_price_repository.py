from pymysql.connections import Connection

from src.infrastructure.mysql.connection.create_connection import create_connection


class SqlLiftPriceRepository:
    TABLE_NAME = "base_price"

    def __init__(self, connection: Connection) -> None:
        self.cursor = connection.cursor()

    def save(self, lift_type: str, cost: float) -> None:
        statement = f"INSERT INTO {self.TABLE_NAME} (type, cost) VALUES (?, ?) ON DUPLICATE KEY UPDATE cost = ?"
        self.cursor.execute(statement, [lift_type, cost, cost])

    def delete(self, lift_type: str) -> None:
        statement = f"DELETE FROM {self.TABLE_NAME} WHERE type = ? "
        self.cursor.execute(statement, lift_type)

    def find_by_type(self, lift_type: str) -> float:
        statement = f"SELECT cost FROM {self.TABLE_NAME} WHERE type = ? "
        self.cursor.execute(statement, [lift_type])
        return float(self.cursor.fetchone()[0])


class SqlLiftPriceRepositoryFactory:
    @staticmethod
    def make() -> SqlLiftPriceRepository:
        connection = create_connection()
        return SqlLiftPriceRepository(connection)
