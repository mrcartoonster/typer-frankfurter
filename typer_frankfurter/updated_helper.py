# -*- coding: utf-8 -*-
import httpx

# import freecurrencyapi
# from environs import Env


# The API KEY is set
# env = Env()


# client = freecurrencyapi.Client(env['API_KEY'])


FRANKFUTER_URL = "https://api.frankfurter.dev/v1/"


def yen_to_usd(
    amount: float = 1000.00,
    # key_money: bool = False,
    **kwargs,
) -> None:

    # 	if key_money:
    # 		amount *= 2
    #
    # Insert Try and Accept
    try:
        jpy = httpx.get(url=FRANKFUTER_URL + "latest", params={"base": "JPY"})
        jpy.raise_for_status()
        yen = jpy.json()
        total_kwargs = list(kwargs.values())
        total_kwargs.append(amount)
        amount = sum(total_kwargs)
    except httpx.HTTPError as exc:
        print(f"Error while requestions {exc.request.url!r}.")

    converted = amount * yen["rates"]["USD"]
    print(f"{amount} yen is ${converted:.2f}.")
