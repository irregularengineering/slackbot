"""
Stock API

Look up companies, prices, returns, etc.
"""

from typing import NamedTuple

from iexfinance import Stock
from iexfinance.utils.exceptions import IEXSymbolError

StockInfo = NamedTuple('StockInfo', [('symbol', str), ('name', str), ('one_day_return', float)])


class SymbolNotFoundError(Exception):
    """
    Thrown when symbol is not valid
    """
    def __init__(self, symbol):
        message = 'Invalid stock symbol: {}'.format(symbol)
        super(SymbolNotFoundError, self).__init__(message)


class StockApi(object):
    """
    Request information about a stock symbol such as company name, price, return, etc.
    """
    @staticmethod
    def get_stock_info(symbol: str) -> StockInfo:
        """
        Fetch quote given stock ticker symbol

        :param symbol: ticker symbol as str
        :return: instance of StockInfo
        """
        try:
            quote = Stock(symbol).get_quote()
        except IEXSymbolError:
            raise SymbolNotFoundError(symbol)
        else:
            return StockInfo(symbol.upper(), quote['companyName'], quote['changePercent'])
