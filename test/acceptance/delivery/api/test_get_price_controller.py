from doublex import Mimic, Spy
from doublex_expects import have_been_called_with
from expects import equal, expect

from src.delivery.api.get_price_controller import GetPriceController
from src.domain.lift_pass_type import LiftPassType
from src.main import app
from src.use_cases.get_price_query_handler import GetPriceQuery, GetPriceQueryHandler


class TestGetPriceControllerAcceptance:
    def test_get_price(self) -> None:
        pass_type = LiftPassType.ONE_JOUR
        age = "18"
        date = "2022-01-01"
        cost = 100
        query_string = {"type": pass_type.value, "age": age, "date": date}
        query = GetPriceQuery(pass_type, age, date)
        expected_response = {"cost": cost}
        with Mimic(Spy, GetPriceQueryHandler) as query_handler:
            query_handler.execute(query).returns(cost)
        get_price_controller = GetPriceController(query_handler)  # type: ignore

        with app.test_request_context(query_string=query_string):
            response = get_price_controller.get_price()

        expect(query_handler.execute).to(have_been_called_with(query))
        expect(response.json).to(equal(expected_response))

    def test_get_price_for_non_existing_type(self) -> None:
        query_string = {"type": "non-existing-type"}
        query_handler = Mimic(Spy, GetPriceQueryHandler)
        expected_response = {"cost": 0}
        get_price_controller = GetPriceController(query_handler)  # type: ignore

        with app.test_request_context(query_string=query_string):
            response = get_price_controller.get_price()

        expect(response.json).to(equal(expected_response))
