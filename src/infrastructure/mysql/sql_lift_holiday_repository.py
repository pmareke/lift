from pymysql.connections import Connection

from src.infrastructure.mysql.connection.create_connection import create_connection


class SqlLiftHolidayRepository:
    def __init__(self, connection: Connection) -> None:
        self.cursor = connection.cursor()

    def is_holiday(self, date: str) -> bool:
        statement = "SELECT 1 FROM holidays WHERE holiday  = ? "
        return bool(self.cursor.execute(statement, date))


class SqlLiftHolidayRepositoryFactory:
    @staticmethod
    def make() -> SqlLiftHolidayRepository:
        connection = create_connection()
        return SqlLiftHolidayRepository(connection)
