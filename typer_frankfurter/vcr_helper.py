# -*- coding: utf-8 -*-
import httpx
import vcr
from rich import print

frankfuter_base_url = "https://api.frankfurter.app/latest"
currencies_url = "https://api.frankfurter.app/currencies"


@vcr.use_cassette("cassettes/japan_call.yaml", record_mode="new_episodes")
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


@vcr.use_cassette(path="cassettes/latest.yaml", record_mode="new_episodes")
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
    path="cassettes/tracked_currencies.yaml",
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
