from dataclasses import dataclass
from pymysql.connections import Connection


@dataclass
class AddPriceCommand:
    lift_pass_type: str
    cost: float


class AddPriceCommandHandler:
    def __init__(self, connection: Connection) -> None:
        self.cursor = connection.cursor()

    def execute(self, command: AddPriceCommand) -> dict:
        type = command.lift_pass_type
        cost = command.cost

        statement = "INSERT INTO `base_price` (type, cost) VALUES (?, ?) ON DUPLICATE KEY UPDATE cost = ?"
        self.cursor.execute(statement, [type, cost, cost])

        return {}
