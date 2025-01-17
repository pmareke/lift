from http.client import CREATED

import pytest
from expects import equal, expect

from src.domain.lift_pass_type import LiftPassType
from src.main import create_app

NIGHT = LiftPassType.NIGHT
ONE_JOUR = LiftPassType.ONE_JOUR


class TestLiftPassAcceptance:
    def setup_method(self) -> None:
        app = create_app()
        self.client = app.test_client()

    def test_add_new_price(self) -> None:
        query_string = {"type": ONE_JOUR.value, "cost": 35}
        response = self.client.put("/prices", query_string=query_string)

        expect(response.status_code).to(equal(CREATED))

    @pytest.mark.parametrize(
        "type",
        [
            ONE_JOUR.value,
            NIGHT.value,
        ],
    )
    def test_people_under_6_does_not_pay(self, type: str) -> None:
        query_string = {"type": type, "age": 5}
        response = self.client.get("/prices", query_string=query_string)

        expect(response.json).to(equal({"cost": 0}))

    def test_is_holiday_and_monday(self) -> None:
        query_string = {"type": ONE_JOUR.value, "date": "2019-02-25"}
        response = self.client.get("/prices", query_string=query_string)

        expect(response.json).to(equal({"cost": 35}))

    def test_is_not_holiday_but_monday(self) -> None:
        query_string = {"type": ONE_JOUR.value, "date": "2024-02-26"}
        response = self.client.get("/prices", query_string=query_string)

        expect(response.json).to(equal({"cost": 23}))

    def test_is_not_monday_but_holiday(self) -> None:
        query_string = {"type": ONE_JOUR.value, "date": "2019-03-05"}
        response = self.client.get("/prices", query_string=query_string)

        expect(response.json).to(equal({"cost": 35}))

    def test_is_neither_holiday_and_monday(self) -> None:
        query_string = {"type": ONE_JOUR.value, "date": "2019-02-15"}
        response = self.client.get("/prices", query_string=query_string)

        expect(response.json).to(equal({"cost": 35}))

    @pytest.mark.parametrize("type,cost", [(ONE_JOUR.value, 35), (NIGHT.value, 0)])
    def test_pass_without_age(self, type: str, cost: int) -> None:
        query_string = {"type": type}
        response = self.client.get("/prices", query_string=query_string)

        expect(response.json).to(equal({"cost": cost}))

    @pytest.mark.parametrize("age,expected_cost", [(10, 25), (65, 27), (50, 35)])
    def test_1jour_pass_with_age(self, age: int, expected_cost: int) -> None:
        query_string = {"type": ONE_JOUR.value, "age": age}
        response = self.client.get("/prices", query_string=query_string)

        expect(response.json).to(equal({"cost": expected_cost}))

    @pytest.mark.parametrize("age,expected_cost", [(10, 19), (65, 8)])
    def test_night_pass_with_age(self, age: int, expected_cost: int) -> None:
        query_string = {"type": NIGHT.value, "age": age}
        response = self.client.get("/prices", query_string=query_string)

        expect(response.json).to(equal({"cost": expected_cost}))
