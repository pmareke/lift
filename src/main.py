from flask import Flask

from src.delivery.api.add_price_controller import AddPriceController
from src.delivery.api.get_price_controller import GetPriceController
from src.infrastructure.mysql.sql_lift_pass_holiday_repository import (
    SqlLiftPassHolidayRepositoryFactory,
)
from src.infrastructure.mysql.sql_lift_pass_repository import (
    SqlLiftPassRepositoryFactory,
)
from src.use_cases.add_price_command_handler import AddPriceCommandHandler
from src.use_cases.get_price_query_handler import GetPriceQueryHandler

app = Flask("lift-pass-pricing")

pass_repository = SqlLiftPassRepositoryFactory.make()
holiday_repository = SqlLiftPassHolidayRepositoryFactory.make()

add_price_command_handler = AddPriceCommandHandler(pass_repository)
add_price_controller = AddPriceController(add_price_command_handler)
app.route("/prices", methods=["PUT"])(add_price_controller.add_price)

get_price_query_handler = GetPriceQueryHandler(pass_repository, holiday_repository)
get_price_controller = GetPriceController(get_price_query_handler)
app.route("/prices", methods=["GET"])(get_price_controller.get_price)


def main() -> None:
    app.run(port=3005)


if __name__ == "__main__":
    main()
