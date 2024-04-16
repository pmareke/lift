from doublex import Mimic, Spy
from doublex_expects import have_been_called_with
from expects import expect, equal

from src.delivery.api.add_price_controller import AddPriceController
from src.main import app
from src.use_cases.add_price_command_handler import AddPriceCommand, AddPriceCommandHandler


class TestAddPriceController:
    def test_add_price(self) -> None:
        lift_pass_type = "1jour"
        cost = 100
        expected_response = {"type": lift_pass_type, "cost": cost}
        command = AddPriceCommand(lift_pass_type, cost)
        with Mimic(Spy, AddPriceCommandHandler) as command_handler:
            command_handler.execute(command).returns(expected_response)
        add_price_controller = AddPriceController(command_handler)  # type: ignore

        with app.test_request_context(query_string=expected_response):
            response = add_price_controller.add_price()

        expect(command_handler.execute).to(have_been_called_with(command))
        expect(response).to(equal(expected_response))
