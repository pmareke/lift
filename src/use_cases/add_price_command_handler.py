from dataclasses import dataclass

from src.domain.lift_pass import LiftPass
from src.domain.lift_pass_type import LiftPassType
from src.infrastructure.mysql.sql_lift_pass_repository import SqlLiftPassRepository


@dataclass
class AddPriceCommand:
    pass_type: LiftPassType
    base_price: float


class AddPriceCommandHandler:
    def __init__(self, lift_pass_repository: SqlLiftPassRepository) -> None:
        self.lift_pass_repository = lift_pass_repository

    def execute(self, command: AddPriceCommand) -> None:
        lift_pass = LiftPass(command.pass_type, command.base_price)
        self.lift_pass_repository.save(lift_pass)
