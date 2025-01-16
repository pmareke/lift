from doublex import Mimic, Spy
from expects import equal, expect

from src.delivery.api.get_prices_controller import GetPricesController
from src.domain.lift_pass_price import LiftPassPrice
from src.domain.lift_pass_type import LiftPassType
from src.main import app
from src.use_cases.get_prices_query_handler import GetPricesQuery, GetPricesQueryHandler


class TestGetPricesController:
    def test_get_prices(self) -> None:
        pass_type = LiftPassType.ONE_JOUR
        age = "18"
        date = "2022-01-01"
        cost = 100
        price = LiftPassPrice(pass_type, age, date)
        query = GetPricesQuery([price])
        expected_response = {"prices": [{"pass_type": pass_type.value, "cost": 100}]}
        payload = {"prices": [{"type": pass_type.value, "age": age, "date": date}]}
        with Mimic(Spy, GetPricesQueryHandler) as query_handler:
            query_handler.execute(query).returns([{"pass_type": pass_type.value, "cost": cost}])
        get_price_controller = GetPricesController(query_handler)  # type: ignore

        with app.test_request_context(json=payload):
            response = get_price_controller.get_prices()

        expect(response.json).to(equal(expected_response))
