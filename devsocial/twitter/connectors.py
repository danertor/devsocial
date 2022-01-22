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


TwitterApiType = type(tweepy.API)


def create_api() -> TwitterApiType:
    auth = tweepy.OAuthHandler(config.TWITTER_API['CONSUMER_KEY'], config.TWITTER_API['CONSUMER_SECRET'])
    auth.set_access_token(config.TWITTER_API['ACCESS_TOKEN'], config.TWITTER_API['ACCESS_TOKEN_SECRET'])
    api = tweepy.API(auth)
    return api


class TwitterApiConnector:
    fields_to_retrieve = 'id'

    def __init__(self, api: TwitterApiType = None):
        self.external_api = api if api else create_api()
        self.config = config.TWITTER_API

    def get_user(self, handle: str) -> TwitterDeveloper:
        twitter_dev_id = self.external_api.get_user(screen_name=handle).id_str
        return TwitterDeveloper(handle, id=twitter_dev_id, followers=self.get_users_followers(handle))

    def get_users_followers(self, handle: str) -> List[TwitterDeveloper]:
        return self.external_api.get_follower_ids(screen_name=handle, stringify_ids=True)
