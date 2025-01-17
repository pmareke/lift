from doublex import Mimic, Spy
from doublex_expects import have_been_called_with
from expects import equal, expect

from src.delivery.api.get_prices_controller import GetPricesController
from src.domain.lift_pass_props import LiftPassProps
from src.domain.lift_pass_type import LiftPassType
from src.main import create_app
from src.use_cases.get_prices_query_handler import GetPricesQuery, GetPricesQueryHandler


class TestGetPricesController:
    def test_get_price(self) -> None:
        app = create_app(test=True)
        pass_type = LiftPassType.ONE_JOUR
        age = "18"
        date = "2022-01-01"
        cost = 100
        payload = {"prices": [{"type": pass_type.value, "age": age, "date": date}]}
        props = LiftPassProps(pass_type, age, date)
        query = GetPricesQuery([props])
        prices = [{"pass_type": pass_type.value, "cost": cost}]
        with Mimic(Spy, GetPricesQueryHandler) as query_handler:
            query_handler.execute(query).returns(prices)
        get_prices_controller = GetPricesController(query_handler)  # type: ignore

        with app.test_request_context(json=payload):
            response = get_prices_controller.get_prices()

        expect(query_handler.execute).to(have_been_called_with(query))

        expected_response = {"prices": prices}
        expect(response.json).to(equal(expected_response))
