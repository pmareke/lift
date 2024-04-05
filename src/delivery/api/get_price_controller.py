import math

from flask import request
from datetime import datetime
from pymysql.connections import Connection


class GetPriceController:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def get_price(self) -> dict:
        res = {}
        cursor = self.connection.cursor()
        cursor.execute(
            f"SELECT cost FROM base_price " + "WHERE type = ? ", (request.args["type"],)
        )
        row = cursor.fetchone()
        result = {"cost": row[0]}
        age = request.args.get("age")
        if age and int(age) < 6:
            res["cost"] = 0
        else:
            if "type" in request.args and request.args["type"] != "night":
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM holidays")
                is_holiday = False
                reduction = 0
                for row in cursor.fetchall():
                    holiday = row[0]
                    if "date" in request.args:
                        d = datetime.fromisoformat(request.args["date"])
                        if (
                            d.year == holiday.year
                            and d.month == holiday.month
                            and holiday.day == d.day
                        ):
                            is_holiday = True
                if (
                    not is_holiday
                    and "date" in request.args
                    and datetime.fromisoformat(request.args["date"]).weekday() == 0
                ):
                    reduction = 35

                # TODO: apply reduction for others
                if age and int(age) < 15:
                    res["cost"] = math.ceil(result["cost"] * 0.7)
                else:
                    if not age:
                        cost = result["cost"] * (1 - reduction / 100)
                        res["cost"] = math.ceil(cost)
                    else:
                        if "age" in request.args and int(age) > 64:
                            cost = result["cost"] * 0.75 * (1 - reduction / 100)
                            res["cost"] = math.ceil(cost)
                        else:
                            cost = result["cost"] * (1 - reduction / 100)
                            res["cost"] = math.ceil(cost)
            else:
                if age and int(age) >= 6:
                    if int(age) > 64:
                        res["cost"] = math.ceil(result["cost"] * 0.4)
                    else:
                        res.update(result)
                else:
                    res["cost"] = 0
        return res
