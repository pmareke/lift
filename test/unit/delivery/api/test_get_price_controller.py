from doublex import Mimic, Spy
from doublex_expects import have_been_called_with
from expects import equal, expect

from src.delivery.api.get_price_controller import GetPriceController
from src.main import app
from src.use_cases.get_price_query_handler import GetPriceQuery, GetPriceQueryHandler


class TestGetPriceController:
    def test_get_price(self) -> None:
        pass_type = "1jour"
        age = "18"
        date = "2022-01-01"
        cost = 100
        query_string = {"type": pass_type, "age": age, "date": date}
        query = GetPriceQuery(pass_type, age, date)
        expected_response = {"cost": cost}
        with Mimic(Spy, GetPriceQueryHandler) as query_handler:
            query_handler.execute(query).returns(cost)
        get_price_controller = GetPriceController(query_handler)  # type: ignore

        with app.test_request_context(query_string=query_string):
            response = get_price_controller.get_price()

        expect(query_handler.execute).to(have_been_called_with(query))
        expect(response).to(equal(expected_response))
