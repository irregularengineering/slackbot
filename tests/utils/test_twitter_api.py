# pylint: disable=missing-docstring
"""
Tests for Twitter API
"""

from slackbot.utils.twitter_api import TwitterApi


def test_twitter_get_stock_tweets():
    twitter = TwitterApi()
    assert isinstance(twitter.get_stock_tweets('TSLA'), list)


def test_clean_tweet():
    assert TwitterApi.clean_tweet(
        "This is from Elon's BROTHER. $TSLA https://t.co/5jlMblw92o"
    ) == 'This is from Elon s BROTHER. TSLA'
    assert TwitterApi.clean_tweet(
        'RT @tslatrack: "Yo that\'s a sick $TSLA. Is that yours? No that\'s my dad\'s.'
    ) == 'RT Yo that s a sick TSLA. Is that yours No that s my dad s.'
