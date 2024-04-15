from datetime import date
from pymysql.connections import Connection
from src.db import create_lift_pass_db_connection


class SqlLiftHolidayRepository:
    def __init__(self, connection: Connection) -> None:
        self.cursor = connection.cursor()

    def is_holiday(self, date: str) -> bool:
        statement = "SELECT 1 FROM holidays WHERE holiday  = ? "
        return bool(self.cursor.execute(statement, date))


class SqlLiftHolidayRepositoryFactory:
    @staticmethod
    def make() -> SqlLiftHolidayRepository:
        connection = create_lift_pass_db_connection()
        return SqlLiftHolidayRepository(connection)
