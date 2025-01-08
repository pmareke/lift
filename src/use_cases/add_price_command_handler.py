from dataclasses import dataclass

from src.infrastructure.mysql.sql_lift_pass_repository import SqlLiftPassRepository


@dataclass
class AddPriceCommand:
    pass_type: str
    base_price: float


class AddPriceCommandHandler:
    def __init__(self, lift_pass_repository: SqlLiftPassRepository) -> None:
        self.lift_pass_repository = lift_pass_repository

    def execute(self, command: AddPriceCommand) -> None:
        pass_type = command.pass_type
        base_price = command.base_price
        self.lift_pass_repository.save(pass_type, base_price)
