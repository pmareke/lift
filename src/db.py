import pymysql.cursors

from pymysql.connections import Connection
from pymysql.cursors import Cursor


class PyMySQLCursorWrapper(Cursor):
    """
    The pymysql.cursors.Cursor class very nearly works the same as the odbc equivalent. Unfortunately it doesn't
    understand the '?' in a SQL statement as an argument placeholder, and instead uses '%s'. This wrapper fixes that.
    """

    def mogrify(self, query: str, args: object = ...) -> str:
        query = query.replace("?", "%s")
        return str(super().mogrify(query, args))


def create_lift_pass_db_connection(connection_options: dict) -> Connection:
    return pymysql.connect(
        host=connection_options["host"],
        user=connection_options["user"],
        password=connection_options["password"],
        database=connection_options["database"],
        cursorclass=PyMySQLCursorWrapper,
    )
