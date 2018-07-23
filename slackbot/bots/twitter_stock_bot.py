"""
Stock Bot

Twitter stock sentiment analyzer

Usage:
    stock_bot = StockBot()
    print(stock_bot.analyze_sentiment('tsla'))
"""

from typing import List, NamedTuple

import numpy as np

from slackbot.utils.twitter_api import TwitterApi
from slackbot.utils.stock_api import StockApi, StockInfo
from slackbot.utils.sentiment_analyzer import SentimentAnalyzer
from slackbot.utils import string_utils

TweetResult = NamedTuple('TweetResult', [('raw', str), ('clean', str), ('sentiment', float)])


class TwitterStockBot(object):
    """
    Find the tweets about a stock and report on return and sentiment
    """
    def __init__(self):
        self.twitter_api = TwitterApi()
        self.stock_api = StockApi()
        self.sentiment_analyzer = SentimentAnalyzer()

    def analyze_sentiment(self, symbol: str) -> str:
        """
        Query Twitter for tweets involving stock ticker symbol and return sentiment analysis

        :param symbol: stock symbol as str
        :return: result as str
        """
        quote = self.stock_api.get_stock_info(symbol)
        results = list()
        for tweet in self.twitter_api.get_stock_tweets(symbol):
            clean_tweet = self.twitter_api.clean_tweet(tweet)
            sentiment = self.sentiment_analyzer.get_sentiment(clean_tweet)
            results.append(TweetResult(raw=tweet, clean=clean_tweet, sentiment=sentiment))
        return self.build_sentiment_message(quote, results)

    @staticmethod
    def build_sentiment_message(stock_info: StockInfo, tweets: List[TweetResult]) -> str:
        """
        Build a string summary of sentiment analysis

        :param stock_info: instance of StockInfo
        :param tweets: list of TweetResults
        :return: summary string of stock name, percent change, and sentiment analysis
        """
        if tweets:
            sentiment = float(np.mean([tweet.sentiment for tweet in tweets]))
            tweet_message = '({:,.0f} tweet{} averaging {}{:.0f}% sentiment)'.format(
                len(tweets),
                string_utils.pluralize(len(tweets)),
                TwitterStockBot.get_sentiment_polarity(sentiment),
                100. * sentiment
            )
        else:
            tweet_message = '(no tweets)'
        return '{} is {} {:,.2f}% {}'.format(
            stock_info.name,
            TwitterStockBot.get_return_polarity(stock_info.one_day_return),
            100. * stock_info.one_day_return,
            tweet_message
        )

    @staticmethod
    def get_return_polarity(percent_return: float) -> str:
        """
        Construct string describing polarity of return

        :param percent_return: as float
        :return: str value of polarity
        """
        if percent_return > 0.:
            return 'up'
        if percent_return < 0.:
            return 'down'
        return 'unchanged at'

    @staticmethod
    def get_sentiment_polarity(sentiment: float) -> str:
        """
        Construct string describing polarity of sentiment

        :param sentiment: as float
        :return: str value of polarity
        """
        if sentiment > 0.:
            return '+'
        if sentiment < 0.:
            return '-'
        return ''
