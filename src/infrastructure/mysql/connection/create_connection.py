from pymysql import connect
from pymysql.connections import Connection

from src.infrastructure.mysql.connection.py_mysql_cursor_wrapper import PyMySQLCursorWrapper


def create_connection() -> Connection:
    try:
        return connect(
            host="mariadb",
            user="root",
            password="mysql",
            database="lift_pass",
            cursorclass=PyMySQLCursorWrapper,
        )
    except Exception as ex:
        print(f"Error connecting to database: {ex}")
