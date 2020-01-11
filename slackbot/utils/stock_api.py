"""
Stock API

Look up companies, prices, returns, etc.
"""

from typing import NamedTuple

from iexfinance.stocks import Stock
from iexfinance.utils.exceptions import IEXQueryError

from slackbot.utils.secrets import Secrets

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
    def __init__(self):
        secrets = Secrets()
        self.token = secrets.get('IEX', 'token')

    def get_stock_info(self, symbol: str) -> StockInfo:
        """
        Fetch quote given stock ticker symbol

        :param symbol: ticker symbol as str
        :return: instance of StockInfo
        """
        try:
            quote = Stock(symbol, token=self.token).get_quote()
        except IEXQueryError:
            raise SymbolNotFoundError(symbol)
        else:
            return StockInfo(symbol.upper(), quote['companyName'], quote['changePercent'])
