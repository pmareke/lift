from flask import Flask

from src.delivery.api.add_price_controller import AddPriceController
from src.delivery.api.get_price_controller import GetPriceController
from src.delivery.api.get_prices_controller import GetPricesController
from src.infrastructure.mysql.sql_lift_pass_holiday_repository import (
    SqlLiftPassHolidayRepositoryFactory,
)
from src.infrastructure.mysql.sql_lift_pass_repository import (
    SqlLiftPassRepositoryFactory,
)
from src.use_cases.add_price_command_handler import AddPriceCommandHandler
from src.use_cases.get_price_query_handler import GetPriceQueryHandler
from src.use_cases.get_prices_query_handler import GetPricesQueryHandler

app = Flask("lift-pass-pricing")

lift_pass_repository = SqlLiftPassRepositoryFactory.make()
lift_pass_holiday_repository = SqlLiftPassHolidayRepositoryFactory.make()

command_handler = AddPriceCommandHandler(lift_pass_repository)
add_price_controller = AddPriceController(command_handler)
app.route("/prices", methods=["PUT"])(add_price_controller.add_price)

price_query_handler = GetPriceQueryHandler(lift_pass_repository, lift_pass_holiday_repository)
get_price_controller = GetPriceController(price_query_handler)
app.route("/prices", methods=["GET"])(get_price_controller.get_price)

prices_query_handler = GetPricesQueryHandler(lift_pass_repository, lift_pass_holiday_repository)
get_prices_controller = GetPricesController(prices_query_handler)
app.route("/prices", methods=["POST"])(get_prices_controller.get_prices)


def main() -> None:
    app.run(port=3005)


if __name__ == "__main__":
    main()
