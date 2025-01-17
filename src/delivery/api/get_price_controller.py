from http.client import OK

from flask import Response, make_response, request

from src.domain.lift_pass_props import LiftPassProps
from src.domain.lift_pass_type import LiftPassType
from src.use_cases.get_price_query_handler import GetPriceQuery, GetPriceQueryHandler


class GetPriceController:
    def __init__(self, query_handler: GetPriceQueryHandler) -> None:
        self.query_handler = query_handler

    def get_price(self) -> Response:
        try:
            pass_type = LiftPassType(request.args["type"])
        except ValueError:
            return make_response({"cost": 0}, OK)

        age = request.args.get("age")
        date = request.args.get("date")
        price = LiftPassProps(pass_type, age, date)
        query = GetPriceQuery(price)

        cost = self.query_handler.execute(query)

        return make_response({"cost": cost}, OK)
