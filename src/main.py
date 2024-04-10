from flask import Flask

from src.db import create_lift_pass_db_connection
from src.delivery.api.get_price_controller import GetPriceController
from src.delivery.api.add_price_controller import AddPriceController
from src.use_cases.add_price_command_handler import AddPriceCommandHandler
from src.use_cases.get_price_query_handler import GetPriceQueryHandler

app = Flask("lift-pass-pricing")

connection = create_lift_pass_db_connection()

command_handler = AddPriceCommandHandler(connection)
add_price_controller = AddPriceController(command_handler)
app.route("/prices", methods=["PUT"])(add_price_controller.add_price)

query_handler = GetPriceQueryHandler(connection)
get_price_controller = GetPriceController(query_handler)
app.route("/prices", methods=["GET"])(get_price_controller.get_price)


def __main__() -> None:
    app.run(port=3005)
