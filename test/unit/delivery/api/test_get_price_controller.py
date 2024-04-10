from doublex import Mimic, Stub
from expects import expect, equal
from src.delivery.api.get_price_controller import GetPriceController
from src.use_cases.get_price_query_handler import GetPriceQuery, GetPriceQueryHandler
from src.main import app


class TestGetPriceController:
    def test_get_price(self) -> None:
        lift_pass_type = "1jour"
        age = "18"
        date = "2022-01-01"
        query_string = {"type": lift_pass_type, "age": age, "date": date}
        query = GetPriceQuery(lift_pass_type, age, date)
        expected_response = {"cost": 100}
        with Mimic(Stub, GetPriceQueryHandler) as query_handler:
            query_handler.execute(query).returns(expected_response)
        get_price_controller = GetPriceController(query_handler)  # type: ignore

        with app.test_request_context(query_string=query_string):
            response = get_price_controller.get_price()

        expect(response).to(equal(expected_response))
