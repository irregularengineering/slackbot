"""
Twitter API

Tools for querying tweets
"""


import re
import html
import logging
from datetime import datetime, timedelta
from typing import List

import pytz

from twitter import Twitter
from twitter import OAuth
from twitter import oauth_dance


from slackbot.utils.secrets import Secrets


class TwitterApi(object):
    """
    Connect to Twitter and query for tweets
    """
    CONFIG_SECTION = 'Twitter'
    TWITTER_DATE_FORMAT = '%a %b %d %H:%M:%S %z %Y'
    TWEET_REGEX = r'(@[A-Za-z0-9]+)|([^0-9A-Za-z,\.])|(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})'\
        r'([\/\w \.-]*)*\/?'
    DEF_MAX_HOURS_OLD = 24

    def __init__(self):
        secrets = Secrets()
        api_key = secrets.get(self.CONFIG_SECTION, 'api_key')
        api_secret = secrets.get(self.CONFIG_SECTION, 'api_secret')
        oauth_token = secrets.get(self.CONFIG_SECTION, 'oauth_token')
        oauth_secret = secrets.get(self.CONFIG_SECTION, 'oauth_secret')
        if not oauth_token or not oauth_secret:
            oauth_token, oauth_secret = oauth_dance('irregular_stock_bot', api_key, api_secret)
        self.twitter = Twitter(
            auth=OAuth(oauth_token, oauth_secret, api_key, api_secret),
            retry=True
        )

    def get_stock_tweets(
            self, symbol: str, max_hours_old: int = DEF_MAX_HOURS_OLD) -> List[str]:
        """
        Call Twitter tweet search API in a loop until we collect all tweets after ref_date

        :param symbol: stock symbol as str
        :param max_hours_old: int value of maximum tweet age in hours
        :return: list of text of tweets
        """
        ref_date = datetime.utcnow().replace(tzinfo=pytz.utc) - timedelta(hours=max_hours_old)
        response = self.twitter.search.tweets(
            q='$' + symbol.upper(),
            lang='en',
            count=100,
            include_entities=False
        )
        logging.debug('Retrieved %s results for %s', len(response['statuses']), symbol)
        tweets = list()
        for tweet in response['statuses']:
            created_at = datetime.strptime(tweet['created_at'], self.TWITTER_DATE_FORMAT)
            if created_at < ref_date:
                return tweets
            tweets.append(tweet['text'])
        return tweets

    @staticmethod
    def clean_tweet(tweet: str) -> str:
        """
        Remove tags, links, and non-alphanumeric text
        :param tweet: as text
        :return: cleaned tweet as text
        """
        return ' '.join(re.sub(TwitterApi.TWEET_REGEX, ' ', html.unescape(tweet)).split())
