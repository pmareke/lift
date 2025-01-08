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
        pass_type = request.args["type"]
        base_price = float(request.args["cost"])
        command = AddPriceCommand(pass_type, base_price)

        self.command_handler.execute(command)

        return Response(status=CREATED)
