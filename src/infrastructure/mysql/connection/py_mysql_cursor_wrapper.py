from pymysql.cursors import Cursor


class PyMySQLCursorWrapper(Cursor):
    """
    The Cursor class doesn't understand the '?' in a SQL statement as an
    argument placeholder, and instead uses '%s'.

    This wrapper fixes that.
    """

    def mogrify(self, query: str, args: object = ...) -> str:
        query = query.replace("?", "%s")
        return str(super().mogrify(query, args))
