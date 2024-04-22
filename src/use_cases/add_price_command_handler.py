from dataclasses import dataclass

from src.infrastructure.mysql.sql_lift_price_repository import SqlLiftPriceRepository


@dataclass
class AddPriceCommand:
    lift_pass_type: str
    cost: float


class AddPriceCommandHandler:
    def __init__(self, lift_price_repository: SqlLiftPriceRepository) -> None:
        self.lift_price_repository = lift_price_repository

    def execute(self, command: AddPriceCommand) -> dict:
        pass_type = command.lift_pass_type
        cost = command.cost

        self.lift_price_repository.save(pass_type, cost)

        return {}
