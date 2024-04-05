from flask import request
from pymysql.connections import Connection


class AddPriceController:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def add_price(self) -> dict:
        lift_pass_cost = request.args["cost"]
        lift_pass_type = request.args["type"]
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO `base_price` (type, cost) VALUES (?, ?) "
            + "ON DUPLICATE KEY UPDATE cost = ?",
            (lift_pass_type, lift_pass_cost, lift_pass_cost),
        )
        return {}
