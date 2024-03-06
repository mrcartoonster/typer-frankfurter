# -*- coding: utf-8 -*-
from pathlib import Path

import httpx
import vcr
from rich import print

frankfuter_base_url = "https://api.frankfurter.app/latest"
currencies_url = "https://api.frankfurter.app/currencies"


test_cassettes = Path(
    "/Users/evanbaird/Projects/Personal_Projects/typer-frankfurter/tests/cassettes/",
)


# Move cassettes to be saved in tests/cassettes!
@vcr.use_cassette(
    path=test_cassettes / "japan_call",
    record_mode="new_episodes",
)
def japan_call(amount: int = 1000):
    param = {
        "amount": amount,
        "from": "JPY",
        "to": "USD",
    }

    with httpx.Client(params=param) as client:
        resp = client.get(url=frankfuter_base_url)

        try:
            resp.raise_for_status()

        except httpx.HTTPStatusError as exc:
            print(f"Got an error: {exc.response.status_code}")

    return resp.json()


@vcr.use_cassette(
    path=test_cassettes / "getting_latest",
    record_mode="new_episodes",
)
def getting_latest(country: str = "USD"):
    from_param = {"from": country.upper()}
    with httpx.Client(params=from_param) as client:
        resp = client.get(url=frankfuter_base_url, params=from_param)

        try:
            resp.raise_for_status()

        except httpx.HTTPStatusError as exc:
            print(f"Got a: {exc.response.status_code} error")

    return resp.json()


@vcr.use_cassette(
    path=test_cassettes / "tracking_call",
    record_mode="new_episodes",
)
def tracking_call():

    with httpx.Client() as client:
        resp = client.get(url=currencies_url)
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            print(
                f"Got an error in tracking_call: {exc.response.status_code}!",
            )

    return resp.json()
