from pymysql.connections import Connection

from src.domain.lift_pass_holiday_repository import LiftPassHolidayRepository
from src.infrastructure.mysql.connection.create_connection import create_connection


class SqlLiftPassHolidayRepository(LiftPassHolidayRepository):
    TABLE_NAME = "holidays"

    def __init__(self, connection: Connection) -> None:
        self.cursor = connection.cursor()

    def is_holiday(self, date: str) -> bool:
        statement = f"SELECT 1 FROM {self.TABLE_NAME} WHERE holiday  = ? "
        return bool(self.cursor.execute(statement, date))


class SqlLiftPassHolidayRepositoryFactory:
    @staticmethod
    def make() -> SqlLiftPassHolidayRepository:
        connection = create_connection()
        return SqlLiftPassHolidayRepository(connection)
