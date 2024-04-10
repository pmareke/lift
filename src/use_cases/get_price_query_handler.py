import math

from dataclasses import dataclass
from datetime import datetime

from pymysql.connections import Connection


@dataclass
class GetPriceQuery:
    liff_pass_type: str
    age: str | None = None
    date: str | None = None


class GetPriceQueryHandler:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def execute(self, query: GetPriceQuery) -> dict:
        res = {}
        cursor = self.connection.cursor()
        cursor.execute(
            f"SELECT cost FROM base_price " + "WHERE type = ? ", (query.liff_pass_type,)
        )
        row = cursor.fetchone()
        result = {"cost": row[0]}
        age = query.age
        if age and int(age) < 6:
            res["cost"] = 0
        else:
            if query.liff_pass_type and query.liff_pass_type != "night":
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM holidays")
                is_holiday = False
                reduction = 0
                for row in cursor.fetchall():
                    holiday = row[0]
                    if query.date:
                        d = datetime.fromisoformat(query.date)
                        if (
                            d.year == holiday.year
                            and d.month == holiday.month
                            and holiday.day == d.day
                        ):
                            is_holiday = True
                if (
                    not is_holiday
                    and query.date
                    and datetime.fromisoformat(query.date).weekday() == 0
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
                        if query.age and int(age) > 64:
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
