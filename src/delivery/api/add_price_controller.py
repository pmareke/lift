from http.client import CREATED

from flask import Response, request

from src.use_cases.add_price_command_handler import (
    AddPriceCommand,
    AddPriceCommandHandler,
)


class AddPriceController:
    def __init__(self, command_handler: AddPriceCommandHandler) -> None:
        self.command_handler = command_handler

    def add_price(self) -> Response:
        lift_pass_type = request.args["type"]
        cost = float(request.args["cost"])
        command = AddPriceCommand(lift_pass_type, cost)

        self.command_handler.execute(command)

        return Response(status=CREATED)
