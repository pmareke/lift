import pytest

from src.main import app


class TestLiftPass:
    def setup_method(self) -> None:
        self.client = app.test_client()

    def test_add_new_price(self) -> None:
        response = self.client.put("/prices", query_string={"type": "test", "cost": 35})

        assert response.status_code == 200

    @pytest.mark.parametrize("type", ["1jour", "night"])
    def test_people_under_6_does_not_pay(self, type: str) -> None:
        response = self.client.get("/prices", query_string={"type": type, "age": 5})

        assert response.json == {"cost": 0}

    def test_is_holiday(self) -> None:
        response = self.client.get(
            "/prices", query_string={"type": "1jour", "date": "2019-02-25"}
        )

        assert response.json == {"cost": 35}

    def test_is_not_holiday(self) -> None:
        response = self.client.get(
            "/prices", query_string={"type": "1jour", "date": "2024-02-26"}
        )

        assert response.json == {"cost": 23}

    @pytest.mark.parametrize(
        "type,cost",
        [
            ("1jour", 35),
            ("night", 0),
        ],
    )
    def test_pass_without_age(self, type: str, cost: int) -> None:
        response = self.client.get("/prices", query_string={"type": type})

        assert response.json == {"cost": cost}

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

        assert response.json == {"cost": expected_cost}

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

        assert response.json == {"cost": expected_cost}
