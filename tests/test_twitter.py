# pylint: disable=missing-module-docstring, disable=missing-class-docstring, missing-function-docstring
# pylint: disable=unused-variable, unused-argument, no-self-use
from unittest.mock import Mock
from typing import List
import pytest

from devsocial.models.base_developer import HandleType
from devsocial.twitter.models import TwitterDeveloper, TwitterDeveloperIdType
from devsocial.twitter.controllers import TwitterConnectedController
from devsocial.twitter.connectors import TwitterApiConnector, create_api, TwitterApiType


def test_twitter_dev_has_followers():
    followers = ([TwitterDeveloper(handle) for handle in ('bart', 'lisa')])
    twitter_dev: TwitterDeveloper = TwitterDeveloper('krasty', followers=followers)
    assert followers[0] in twitter_dev.followers


def test_twitter_dev_has_no_followers():
    twitter_dev: TwitterDeveloper = TwitterDeveloper('moleman')
    assert not twitter_dev.followers


def test_two_developers_are_twitter_connected():
    twitter_dev1: TwitterDeveloper = TwitterDeveloper('homer', id='1')
    twitter_dev2: TwitterDeveloper = TwitterDeveloper('mrburns', id='2')
    twitter_dev1.followers.append(twitter_dev2.id)
    twitter_dev2.followers.append(twitter_dev1.id)
    twitter_net: TwitterConnectedController = TwitterConnectedController()
    assert twitter_net.connected(twitter_dev1, twitter_dev2)


def test_two_developers_are_not_twitter_connected():
    twitter_dev1: TwitterDeveloper = TwitterDeveloper('homer', id='1')
    twitter_dev2: TwitterDeveloper = TwitterDeveloper('flanders', id='2')
    twitter_dev2.followers.append(twitter_dev1.id)
    twitter_net: TwitterConnectedController = TwitterConnectedController()
    assert not twitter_net.connected(twitter_dev1, twitter_dev2)


def test_check_same_developer_twitter_connected():
    twitter_dev1: TwitterDeveloper = TwitterDeveloper('homer')
    twitter_net: TwitterConnectedController = TwitterConnectedController()
    assert not twitter_net.connected(twitter_dev1, twitter_dev1)


class TestTwitterConnector:
    twitter_dev_handle: HandleType = 'homer'
    twitter_dev_id: TwitterDeveloperIdType = '1'
    follower_handle: HandleType = 'lenny'
    follower_id: TwitterDeveloperIdType = '2'

    @pytest.fixture
    def twitter_api(self) -> TwitterApiType:
        api = create_api()
        return api

    def mock_get_user(self, screen_name: str, *ignored_arg, **ignored_kwargs) -> Mock:
        mock_follower_response = Mock()
        mock_follower_response.id_str = self.twitter_dev_id
        return mock_follower_response

    def mock_get_follower_ids(self, screen_name: str, *ignored_arg, **ignored_kwargs) -> List[TwitterDeveloperIdType]:
        return [self.follower_id, ]

    def test_get_developers_followers(self, monkeypatch, twitter_api: TwitterApiType):
        monkeypatch.setattr(twitter_api, "get_follower_ids", self.mock_get_follower_ids, raising=False)
        twitter_connector = TwitterApiConnector(twitter_api)
        twitter_dev_followers = twitter_connector.get_users_followers(self.twitter_dev_handle)
        assert twitter_dev_followers[0] == self.follower_id

    def test_get_user(self, monkeypatch, twitter_api: TwitterApiType):
        monkeypatch.setattr(twitter_api, "get_user", self.mock_get_user)
        monkeypatch.setattr(twitter_api, "get_follower_ids", self.mock_get_follower_ids, raising=False)
        twitter_connector = TwitterApiConnector(twitter_api)
        twitter_dev = twitter_connector.get_user(self.twitter_dev_handle)
        assert twitter_dev.handle == self.twitter_dev_handle
        assert twitter_dev.id == self.twitter_dev_id


@pytest.mark.skip(reason="Disable external api communication")
class TestTwitterExternalApi:
    twitter_dev_handle = 'ULLEstudiantes'
    twitter_dev_id = '1479961174594793486'
    follower_id = '917540588'

    @pytest.fixture
    def twitter_api(self) -> TwitterApiType:
        api = create_api()
        return api

    def test_get_developers_followers(self, twitter_api: TwitterApiType):
        twitter_connector = TwitterApiConnector(twitter_api)
        twitter_dev_followers = twitter_connector.get_users_followers(self.twitter_dev_handle)
        assert self.follower_id in twitter_dev_followers

    def test_get_user(self, twitter_api: TwitterApiType):
        twitter_connector = TwitterApiConnector(twitter_api)
        twitter_dev = twitter_connector.get_user(self.twitter_dev_handle)
        assert twitter_dev.id == self.twitter_dev_id
