# -*- coding: utf-8 -*-

import typer
from typing_extensions import Annotated

from typer_frankfurter.vcr_main import japan_to_us, latest, tracked_currencies

# from typer_frankfurter.helper import japan_to_us, latest, tracked_currencies


app = typer.Typer(help="CLI for currency exchange rates")


@app.command()
def yen_to_usd(
    amount: Annotated[
        int,
        typer.Argument(help="Quick Japanese to USD conversion"),
    ] = 1000,
) -> None:
    """
    Converts Japanese Yen to US Dollars.
    """
    return japan_to_us(amount=amount)


@app.command()
def latest_rates(
    currency: Annotated[
        str,
        typer.Argument(
            help="Default is US Dollars. Can be change to another base currency.",
        ),
    ] = "USD",
):
    """
    Latest rates.

    Based on USD. Can be change to another supported currency to base
    exchange rate.

    """
    return latest(frm=currency)


@app.command()
def currencies():
    """
    Currencies that are available to view.
    """
    return tracked_currencies()
