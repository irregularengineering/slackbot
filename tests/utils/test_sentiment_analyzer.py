# pylint: disable=missing-docstring
"""
Test Sentiment Analyzer
"""

from slackbot.utils.sentiment_analyzer import SentimentAnalyzer


def test_get_sentiment_positive():
    assert SentimentAnalyzer.get_sentiment('Everything is great') > 0
    assert SentimentAnalyzer.get_sentiment('I love ponies') > 0


def test_get_sentiment_negative():
    assert SentimentAnalyzer.get_sentiment('Everything is broken') < 0
    assert SentimentAnalyzer.get_sentiment('I hate ponies') < 0
