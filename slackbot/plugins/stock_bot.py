# pylint: disable=no-self-use,too-many-ancestors
"""
Twitter stock sentiment analyzer
"""

import re

from errbot import BotPlugin, re_botcmd, arg_botcmd

from slackbot.bots.twitter_stock_bot import TwitterStockBot


class StockBot(BotPlugin):
    """
    Analyze the sentiment of tweets about stocks
    """
    @re_botcmd(pattern=r'stock', re_cmd_name_help='stock', flags=re.IGNORECASE)
    @arg_botcmd('symbol', type=str)
    def stock(self, _msg, symbol):
        """
        Analyze the sentiment of tweets about stocks
        """
        return TwitterStockBot().analyze_sentiment(symbol)
