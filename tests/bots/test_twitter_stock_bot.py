# pylint: disable=missing-docstring,redefined-outer-name,invalid-name
"""
Tests for Twitter Stock Bot
"""

import pytest

from slackbot.utils.stock_api import StockInfo, SymbolNotFoundError
from slackbot.bots.twitter_stock_bot import TwitterStockBot, TweetResult


@pytest.fixture
def stock_info():
    return StockInfo('TSLA', 'Tesla, Inc.', 0.025)


@pytest.fixture
def tweets():
    return [
        TweetResult('#!@$ This is great', 'This is great', 0.5),
        TweetResult('This is bad #!@$ ', 'This is bad', -0.5),
        TweetResult('This is ok ////?', 'This is ok', 0.1),
    ]


def test_get_sentiment_direction():
    assert TwitterStockBot.get_sentiment_direction(0.8) == '+'
    assert TwitterStockBot.get_sentiment_direction(-0.8) == '-'
    assert TwitterStockBot.get_sentiment_direction(0.) == ''


def test_get_return_direction():
    assert TwitterStockBot.get_return_direction(0.03) == 'up'
    assert TwitterStockBot.get_return_direction(-0.03) == 'down'
    assert TwitterStockBot.get_return_direction(0.) == 'unchanged at'


def test_build_sentiment_message(stock_info, tweets):
    assert TwitterStockBot.build_sentiment_message(stock_info, tweets) == \
        'Tesla, Inc. is up 2.50% (3 tweets averaging +3% sentiment)'


def test_analyze_sentiment():
    assert 'Tesla' in TwitterStockBot().analyze_sentiment('TSLA')


def test_analyze_sentiment_not_found():
    with pytest.raises(SymbolNotFoundError):
        TwitterStockBot().analyze_sentiment('BOJACK')
