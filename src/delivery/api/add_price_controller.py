from flask import request

from src.use_cases.add_price_command_handler import AddPriceCommand, AddPriceCommandHandler


class AddPriceController:
    def __init__(self, command_handler: AddPriceCommandHandler) -> None:
        self.command_handler = command_handler

    def add_price(self) -> dict:
        lift_pass_type = request.args["type"]
        cost = float(request.args["cost"])
        command = AddPriceCommand(lift_pass_type, cost)
        return self.command_handler.execute(command)
