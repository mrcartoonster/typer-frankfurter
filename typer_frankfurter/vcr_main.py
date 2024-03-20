# -*- coding: utf-8 -*-
import pendulum as p
from rich import print
from rich.console import Console
from rich.table import Table

from typer_frankfurter.vcr_helper import (
    getting_latest,
    japan_call,
    tracking_call,
)


def japan_to_us(amount: int = 1000) -> None:

    current = japan_call(amount=amount)

    rate = round(current["rates"]["USD"], 2)

    date = p.now().to_day_datetime_string()

    print(
        f"The amount of {amount:,} in Japanese :yen: to American :dollar: is: [bold green]$[/]{rate:,}. "
        f"This is as of: {date}.",
    )


def latest(frm: str = "USD"):
    """
    Outputting the latest rates.
    """
    rates = getting_latest(country=frm)

    rate_dict = rates

    table = Table(
        title=f"[bold]Current Exchange Rate[/]. Using: [green]{rate_dict['base']}[/]",
        caption=f'As of: {rate_dict["date"]}',
    )

    table.add_column("[bold grey70]Country[/]", style="magenta")
    table.add_column("[bold grey70]Rates[/]", style="green")

    for _ in rate_dict["rates"].items():
        table.add_row(str(_[0]), str(_[1]))

    console = Console()
    rate_table = console.print(table)

    return rate_table


def tracked_currencies():
    """
    This will output the currencies that are available.
    """
    currency = tracking_call()

    cur = currency

    table = Table(title="Currencies that are tracked")

    table.add_column("Abbr", style="magenta")
    table.add_column("Currency Name", style="green")

    for _ in cur.items():
        table.add_row(str(_[0]), str(_[1]))
    console = Console()
    currency_table = console.print(table)

    return currency_table
