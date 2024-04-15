from flask import Flask

from src.db import create_lift_pass_db_connection
from src.delivery.api.get_price_controller import GetPriceController
from src.delivery.api.add_price_controller import AddPriceController
from src.infrastructure.mysql.sql_lift_price_repository import (
    SqlLiftPriceRepositoryFactory,
)
from src.infrastructure.mysql.sql_lift_holiday_repository import (
    SqlLiftHolidayRepositoryFactory,
)
from src.use_cases.add_price_command_handler import AddPriceCommandHandler
from src.use_cases.get_price_query_handler import GetPriceQueryHandler

app = Flask("lift-pass-pricing")

lift_price_repository = SqlLiftPriceRepositoryFactory.make()
lift_holiday_repository = SqlLiftHolidayRepositoryFactory.make()

command_handler = AddPriceCommandHandler(lift_price_repository)
add_price_controller = AddPriceController(command_handler)
app.route("/prices", methods=["PUT"])(add_price_controller.add_price)

query_handler = GetPriceQueryHandler(lift_price_repository, lift_holiday_repository)
get_price_controller = GetPriceController(query_handler)
app.route("/prices", methods=["GET"])(get_price_controller.get_price)


def __main__() -> None:
    app.run(port=3005)
