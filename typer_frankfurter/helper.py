# -*- coding: utf-8 -*-
from dataclasses import dataclass

import httpx
import pendulum as p
from rich import print
from rich.console import Console
from rich.table import Table

u = "https://api.frankfurter.dev/"


def japan_to_us(amount: int = 1000) -> None:
    param = {
        "amount": amount,
        "from": "JPY",
        "to": "USD",
    }

    current = httpx.get(url=u, params=param).json()

    rate = round(current["rates"]["USD"], 2)

    date = p.now().to_day_datetime_string()

    print(
        f"""
        The amount of {amount} in Japanese :yen: to American \
        :dollar: is: [bold green]$[/]{rate:,}.\
        This is as of: {date}.
        """,
    )


def latest(frm: str = "USD"):
    """
    Outputting the latest rates.
    """
    from_param = {"from": frm.upper()}
    rates = httpx.get(u, params=from_param)

    rate_dict = rates.json()

    table = Table(
        title=f"[bold]Current Exchange Rate[/]. Using: [green]{rate_dict['base']}[/]",
        caption=f"As of: {rate_dict['date']}",
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
    currency = httpx.get(url="https://api.frankfurter.app/currencies").json()

    cur = currency

    table = Table(title="Currencies that are tracked")

    table.add_column("Abbr", style="magenta")
    table.add_column("Currency Name", style="green")

    for _ in cur.items():
        table.add_row(str(_[0]), str(_[1]))
    console = Console()
    currency_table = console.print(table)

    return currency_table


@dataclass
class Conversion:
    """
    Class that outputs Currencies trakced and simple Conversion.
    """

    base: str = "BRL"
    to: str = "USD"

    @staticmethod
    def currencies():
        """
        Return current currency rates against the base.
        """
        with httpx.Client() as client:
            try:
                r = client.get("https://api.frankfurter.dev/v1/currencies")
                r.raise_for_status()
                print(r.json())
            except httpx.HTTPError as exc:
                print(f"Error while requestiong {exc.request.url!r}.")

    def convert(self, amount: float):
        """
        Returns the exchange rate of the base towards the to.
        """
        with httpx.Client() as client:
            params = {"base": self.base, "symbols": self.to}
            r = client.get(
                "https://api.frankfurter.dev/v1/latest",
                params=params,
            )

            c = r.json()
            total = c["rates"][self.to] * amount
            print(f"The {amount} in {self.base} is {total:.2f} in {self.to}")

    def rates(self):
        """
        Returns Rates for the base against all currencies.
        """
        with httpx.Client() as client:
            params = {"base": self.base}
            r = client.get(
                "https://api.frankfurter.dev/v1/latest",
                params=params,
            )
        print(r.json())
