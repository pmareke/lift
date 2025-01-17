from http.client import OK

from flask import Response, make_response, request

from src.domain.lift_pass_props import LiftPassProps
from src.domain.lift_pass_type import LiftPassType
from src.use_cases.get_prices_query_handler import GetPricesQuery, GetPricesQueryHandler


class GetPricesController:
    def __init__(self, query_handler: GetPricesQueryHandler) -> None:
        self.query_handler = query_handler

    def get_prices(self) -> Response:
        props: list[LiftPassProps] = []
        json_prices: list = request.get_json()["prices"]
        for price in json_prices:
            try:
                lift_pass_props = self._generate_lift_pass_props(price)
            except ValueError:
                return make_response({"cost": 0}, OK)
            props.append(lift_pass_props)
        query = GetPricesQuery(props)

        prices = self.query_handler.execute(query)

        return make_response({"prices": prices}, OK)

    def _generate_lift_pass_props(self, price: dict) -> LiftPassProps:
        pass_type = LiftPassType(price["type"])
        age = price.get("age")
        date = price.get("date")
        return LiftPassProps(pass_type, age, date)
