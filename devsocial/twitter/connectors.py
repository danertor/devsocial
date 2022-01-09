# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-few-public-methods
"""
Our Interface for Twitter.
"""
from typing import List
import tweepy

from devsocial import config
from .models import TwitterDeveloper


def create_api() -> tweepy.API:
    auth = tweepy.OAuthHandler(config.TWITTER_API['CONSUMER_KEY'], config.TWITTER_API['CONSUMER_SECRET'])
    auth.set_access_token(config.TWITTER_API['ACCESS_TOKEN'], config.TWITTER_API['ACCESS_TOKEN_SECRET'])
    api = tweepy.API(auth)
    return api


class TwitterApiConnector:
    fields_to_retrieve = 'id'

    def __init__(self, api: tweepy.API):
        self.external_api = api
        self.config = config.TWITTER_API

    def get_users_followers(self, follower_id: str, **kwargs) -> List[TwitterDeveloper]:
        followers = self.external_api.get_users_followers(follower_id,
                                                          max_results=self.config.get('MAX_RESULTS'),
                                                          *kwargs)
        return [TwitterDeveloper(follower.id) for follower in followers]
