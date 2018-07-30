"""
Sentiment Analyzer

Determine the sentiment -1 (negative) to 1 (positive) for a block of text

See: https://planspace.org/20150607-textblob_sentiment/
"""

from textblob import TextBlob


class SentimentAnalyzer(object):
    """
    Analyze the sentiment of a block of text
    """
    @staticmethod
    def get_sentiment(text: str) -> float:
        """
        Return a float -1 to 1 that gauges the sentiment of a message

        :param text: any block of text
        :return: sentiment as float
        """
        return TextBlob(text).polarity
