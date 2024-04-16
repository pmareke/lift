from pymysql.connections import Connection

from src.infrastructure.mysql.connection.create_connection import create_connection


class SqlLiftPriceRepository:
    def __init__(self, connection: Connection) -> None:
        self.cursor = connection.cursor()

    def save(self, lift_type: str, cost: int) -> None:
        statement = "INSERT INTO base_price (type, cost) VALUES (?, ?) ON DUPLICATE KEY UPDATE cost = ?"
        self.cursor.execute(statement, [lift_type, cost, cost])

    def get_by_type(self, lift_type: str) -> float:
        statement = "SELECT cost FROM base_price WHERE type = ? "
        self.cursor.execute(statement, [lift_type])
        return float(self.cursor.fetchone()[0])


class SqlLiftPriceRepositoryFactory:
    @staticmethod
    def make() -> SqlLiftPriceRepository:
        connection = create_connection()
        return SqlLiftPriceRepository(connection)
