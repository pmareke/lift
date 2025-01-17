from doublex import Mimic, Stub
from flask import Flask

from src.delivery.api.add_price_controller import AddPriceController
from src.delivery.api.get_price_controller import GetPriceController
from src.infrastructure.mysql.sql_lift_pass_holiday_repository import (
    SqlLiftPassHolidayRepository,
    SqlLiftPassHolidayRepositoryFactory,
)
from src.infrastructure.mysql.sql_lift_pass_repository import (
    SqlLiftPassRepository,
    SqlLiftPassRepositoryFactory,
)
from src.use_cases.add_price_command_handler import AddPriceCommandHandler
from src.use_cases.get_price_query_handler import GetPriceQueryHandler


def create_app(test: bool = False) -> Flask:
    app = Flask("lift-pass-pricing")

    pass_repository = Mimic(Stub, SqlLiftPassRepository)
    holiday_repository = Mimic(Stub, SqlLiftPassHolidayRepository)
    if not test:
        pass_repository = SqlLiftPassRepositoryFactory.make()
        holiday_repository = SqlLiftPassHolidayRepositoryFactory.make()

    add_price_command_handler = AddPriceCommandHandler(pass_repository)  # type: ignore
    add_price_controller = AddPriceController(add_price_command_handler)
    app.route("/prices", methods=["PUT"])(add_price_controller.add_price)

    get_price_query_handler = GetPriceQueryHandler(pass_repository, holiday_repository)  # type: ignore
    get_price_controller = GetPriceController(get_price_query_handler)
    app.route("/prices", methods=["GET"])(get_price_controller.get_price)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
