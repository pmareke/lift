from http.client import OK

from flask import Response, make_response, request

from src.domain.lift_pass_price import LiftPassPrice
from src.domain.lift_pass_type import LiftPassType
from src.use_cases.get_prices_query_handler import GetPricesQuery, GetPricesQueryHandler


class GetPricesController:
    def __init__(self, query_handler: GetPricesQueryHandler) -> None:
        self.query_handler = query_handler

    def get_prices(self) -> Response:
        try:
            prices: list[dict] = request.get_json()["prices"]
            lift_pass_prices = []
            for price in prices:
                pass_type = LiftPassType(price["type"])
                age = price.get("age")
                date = price.get("date")
                lift_pass_price = LiftPassPrice(pass_type, age, date)
                lift_pass_prices.append(lift_pass_price)
            query = GetPricesQuery(lift_pass_prices)
        except ValueError:
            return make_response({"cost": 0}, OK)

        prices = self.query_handler.execute(query)

        return make_response({"prices": prices}, OK)
