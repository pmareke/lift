import multiprocessing
import time
from typing import Generator

import pytest
import requests

from src.main import app

TEST_PORT = 3006


def server(port: int) -> None:
    app.run(port=port)


def wait_for_server_to_start(server_url: str) -> None:
    started = False
    while not started:
        try:
            requests.get(server_url)
            started = True
        except Exception:
            time.sleep(0.2)


@pytest.fixture(autouse=True, scope="session")
def lift_pass_pricing_app() -> Generator:
    """starts the lift pass pricing flask app running on localhost"""
    p = multiprocessing.Process(target=server, args=(TEST_PORT,))
    p.start()
    server_url = f"http://127.0.0.1:{TEST_PORT}"
    wait_for_server_to_start(server_url)
    yield server_url
    p.terminate()


def test_something(lift_pass_pricing_app: str) -> None:
    response = requests.get(f"{lift_pass_pricing_app}/prices", params={"type": "1jour"})

    assert response.json() == {"cost": 35}
