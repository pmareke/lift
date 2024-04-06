from flask import Flask

from src.db import create_lift_pass_db_connection
from src.delivery.api.get_price_controller import GetPriceController
from src.delivery.api.add_price_controller import AddPriceController

app = Flask("lift-pass-pricing")

connection = create_lift_pass_db_connection()

add_price_controller = AddPriceController(connection)
app.route("/prices", methods=["PUT"])(add_price_controller.add_price)

get_price_controller = GetPriceController(connection)
app.route("/prices", methods=["GET"])(get_price_controller.get_price)


def __main__() -> None:
    app.run(port=3005)
