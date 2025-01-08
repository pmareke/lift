from doublex import Mimic, Spy
from doublex_expects import have_been_called_with
from expects import expect

from src.infrastructure.mysql.sql_lift_pass_repository import SqlLiftPassRepository
from src.use_cases.add_price_command_handler import (
    AddPriceCommand,
    AddPriceCommandHandler,
)


class TestAddPriceCommandHandler:
    def test_add_price_command_handler(self) -> None:
        repository = Mimic(Spy, SqlLiftPassRepository)
        base_price = 100
        lift_pass_type = "day"
        command = AddPriceCommand(lift_pass_type, base_price)
        handler = AddPriceCommandHandler(repository)

        handler.execute(command)

        expect(repository.save).to(have_been_called_with(lift_pass_type, base_price))
