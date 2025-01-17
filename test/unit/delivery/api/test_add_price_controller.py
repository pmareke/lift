from doublex import Mimic, Spy
from doublex_expects import have_been_called_with
from expects import expect

from src.delivery.api.add_price_controller import AddPriceController
from src.domain.lift_pass_type import LiftPassType
from src.main import create_app
from src.use_cases.add_price_command_handler import (
    AddPriceCommand,
    AddPriceCommandHandler,
)


class TestAddPriceControllerAcceptance:
    def test_add_price(self) -> None:
        app = create_app(test=True)
        pass_type = LiftPassType.ONE_JOUR
        cost = 100
        expected_response = {"type": pass_type.value, "cost": cost}
        command = AddPriceCommand(pass_type, cost)
        with Mimic(Spy, AddPriceCommandHandler) as command_handler:
            command_handler.execute(command).returns(expected_response)
        add_price_controller = AddPriceController(command_handler)  # type: ignore

        with app.test_request_context(query_string=expected_response):
            add_price_controller.add_price()

        expect(command_handler.execute).to(have_been_called_with(command))
