# -*- coding: utf-8 -*-
# Tests for japan_to_usd
from typer.testing import CliRunner

from typer_frankfurter.main import app

runner = CliRunner()


def test_japan():
    result = runner.invoke(app, ["yen-to-usd"])
    assert result.exit_code == 0


def test_yen():
    """
    Test amount.
    """
    pass
