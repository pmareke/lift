from http.client import OK
import pytest

from expects import expect, equal
from src.main import app


class TestLiftPass:
    def setup_method(self) -> None:
        self.client = app.test_client()

    def test_add_new_price(self) -> None:
        response = self.client.put("/prices", query_string={"type": "test", "cost": 35})

        expect(response.status_code).to(equal(OK))

    @pytest.mark.parametrize("type", ["1jour", "night"])
    def test_people_under_6_does_not_pay(self, type: str) -> None:
        response = self.client.get("/prices", query_string={"type": type, "age": 5})

        expect(response.json).to(equal({"cost": 0}))

    def test_is_holiday(self) -> None:
        response = self.client.get(
            "/prices", query_string={"type": "1jour", "date": "2019-02-25"}
        )

        expect(response.json).to(equal({"cost": 35}))

    def test_is_not_holiday(self) -> None:
        response = self.client.get(
            "/prices", query_string={"type": "1jour", "date": "2024-02-26"}
        )

        expect(response.json).to(equal({"cost": 23}))

    @pytest.mark.parametrize(
        "type,cost",
        [
            ("1jour", 35),
            ("night", 0),
        ],
    )
    def test_pass_without_age(self, type: str, cost: int) -> None:
        response = self.client.get("/prices", query_string={"type": type})

        expect(response.json).to(equal({"cost": cost}))

    @pytest.mark.parametrize(
        "age,expected_cost",
        [
            (10, 25),
            (65, 27),
            (50, 35),
        ],
    )
    def test_1jour_pass_with_age(self, age: int, expected_cost: int) -> None:
        response = self.client.get(
            "/prices", query_string={"type": "1jour", "age": age}
        )

        expect(response.json).to(equal({"cost": expected_cost}))

    @pytest.mark.parametrize(
        "age,expected_cost",
        [
            (10, 19),
            (65, 8),
        ],
    )
    def test_night_pass_with_age(self, age: int, expected_cost: int) -> None:
        response = self.client.get(
            "/prices", query_string={"type": "night", "age": age}
        )

        expect(response.json).to(equal({"cost": expected_cost}))
