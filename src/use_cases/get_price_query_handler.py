import math

from dataclasses import dataclass
from datetime import datetime

from pymysql.connections import Connection

from src.infrastructure.mysql.sql_lift_price_repository import SqlLiftPriceRepository
from src.infrastructure.mysql.sql_lift_holiday_repository import SqlLiftHolidayRepository


@dataclass
class GetPriceQuery:
    liff_pass_type: str
    age: str | None = None
    date: str | None = None


class GetPriceQueryHandler:
    def __init__(
        self,
        lift_price_repository: SqlLiftPriceRepository,
        lift_holiday_repository: SqlLiftHolidayRepository,
    ) -> None:
        self.lift_price_repository = lift_price_repository
        self.lift_holiday_repository = lift_holiday_repository

    def execute(self, query: GetPriceQuery) -> dict:
        type = query.liff_pass_type
        age = query.age
        date = query.date

        cost = self.lift_price_repository.get_by_type(type)
        result = {"cost": cost}

        res: dict[str, float] = {}
        if age and int(age) < 6:
            res["cost"] = 0
        else:
            if type and type != "night":
                reduction = 0
                if date:
                    iso_date = datetime.fromisoformat(date)
                    is_holiday = self.lift_holiday_repository.is_holiday(date)
                    if not is_holiday and iso_date.weekday() == 0:
                        reduction = 35

                # TODO: apply reduction for others
                if age and int(age) < 15:
                    res["cost"] = math.ceil(result["cost"] * 0.7)
                else:
                    if not age:
                        cost = result["cost"] * (1 - reduction / 100)
                        res["cost"] = math.ceil(cost)
                    else:
                        if age and int(age) > 64:
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
