from pymysql import connect

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


def create_lift_pass_db_connection() -> Connection:
    return connect(
        host="mariadb",
        user="root",
        password="mysql",
        database="lift_pass",
        cursorclass=PyMySQLCursorWrapper,
    )
