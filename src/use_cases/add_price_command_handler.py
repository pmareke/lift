from dataclasses import dataclass
from pymysql.connections import Connection

from src.infrastructure.mysql.sql_lift_price_repository import SqlLiftPriceRepository


@dataclass
class AddPriceCommand:
    lift_pass_type: str
    cost: float


class AddPriceCommandHandler:
    def __init__(self, lift_price_repository: SqlLiftPriceRepository) -> None:
        self.lift_price_repository = lift_price_repository

    def execute(self, command: AddPriceCommand) -> dict:
        type = command.lift_pass_type
        cost = int(command.cost)
        self.lift_price_repository.save(type, cost)
        return {}
