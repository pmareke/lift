from flask import request
from src.use_cases.get_price_query_handler import GetPriceQuery, GetPriceQueryHandler


class GetPriceController:
    def __init__(self, query_handler: GetPriceQueryHandler) -> None:
        self.query_handler = query_handler

    def get_price(self) -> dict:
        lift_pass_type = request.args["type"]
        age = request.args.get("age")
        date = request.args.get("date")
        query = GetPriceQuery(lift_pass_type, age, date)
        return self.query_handler.execute(query)
