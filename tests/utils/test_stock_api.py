# pylint: disable=missing-docstring
"""
Tests for StockApi
"""

import pytest


from slackbot.utils.stock_api import StockApi
from slackbot.utils.stock_api import SymbolNotFoundError


def test_get_info():
    stock_info = StockApi().get_stock_info('TSLA')
    assert stock_info.symbol == 'TSLA'
    assert stock_info.name.startswith('Tesla')
    assert isinstance(stock_info.one_day_return, float)


def test_get_info_not_found():
    with pytest.raises(SymbolNotFoundError):
        StockApi().get_stock_info('BOJACK')
