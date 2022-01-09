# pylint: disable=missing-module-docstring, disable=missing-class-docstring, missing-function-docstring
# pylint: disable=unused-variable, unused-argument

from unittest.mock import Mock
import tweepy

from devsocial.twitter.connectors import TwitterApiConnector
from devsocial.twitter.controllers import TwitterConnectedController
from devsocial.twitter.models import TwitterDeveloper


def test_twitter_dev_has_followers():
    followers = ([TwitterDeveloper(handle) for handle in ('bart', 'lisa')])
    twitter_dev: TwitterDeveloper = TwitterDeveloper('krasty', followers=followers)
    assert followers[0] in twitter_dev.followers


def test_twitter_dev_has_no_followers():
    twitter_dev: TwitterDeveloper = TwitterDeveloper('moleman')
    assert not twitter_dev.followers


def test_two_developers_are_twitter_connected():
    twitter_dev1: TwitterDeveloper = TwitterDeveloper('homer')
    twitter_dev2: TwitterDeveloper = TwitterDeveloper('mrburns')
    twitter_dev1.followers.append(twitter_dev2)
    twitter_dev2.followers.append(twitter_dev1)
    twitter_net: TwitterConnectedController = TwitterConnectedController()
    assert twitter_net.connected(twitter_dev1, twitter_dev2)


def test_two_developers_are_not_twitter_connected():
    twitter_dev1: TwitterDeveloper = TwitterDeveloper('homer')
    twitter_dev2: TwitterDeveloper = TwitterDeveloper('flanders')
    twitter_dev2.followers.append(twitter_dev1)
    twitter_net: TwitterConnectedController = TwitterConnectedController()
    assert not twitter_net.connected(twitter_dev1, twitter_dev2)


def test_check_same_developer_twitter_connected():
    twitter_dev1: TwitterDeveloper = TwitterDeveloper('homer')
    twitter_net: TwitterConnectedController = TwitterConnectedController()
    assert not twitter_net.connected(twitter_dev1, twitter_dev1)


class TestTwitterConnector:
    handle = 'homer'
    follower_handle = 'lenny'

    def mock_get_users_followers(self, _id: str, *args, **kwargs):
        mock_follower_response = Mock()
        mock_follower_response.id = self.follower_handle
        return [mock_follower_response, ]

    def test_get_developers_followers(self, monkeypatch):
        twitter_follower = TwitterDeveloper(self.follower_handle)
        twitter_api = tweepy.Client()
        monkeypatch.setattr(twitter_api, "get_users_followers", self.mock_get_users_followers)
        twitter_connector = TwitterApiConnector(twitter_api)
        twitter_dev_followers = twitter_connector.get_users_followers(self.handle)
        assert twitter_dev_followers[0] == twitter_follower
