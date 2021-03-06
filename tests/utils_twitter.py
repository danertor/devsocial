# pylint: disable=missing-module-docstring, disable=missing-class-docstring, missing-function-docstring
# pylint: disable=unused-variable, unused-argument, no-self-use
from unittest.mock import Mock
import pytest

from devsocial.twitter.connectors import TwitterApiConnector, create_api, TwitterApiType


@pytest.fixture
def mock_get_user(request) -> Mock:
    twitter_dev_id = request.param
    mock_follower_response = Mock()
    mock_follower_response.id_str = twitter_dev_id
    return mock_follower_response


def mock_external_twitter_api_on_connector(monkeypatch, mock_data: dict) -> TwitterApiType:
    twitter_api = create_api()
    monkeypatch.setattr(twitter_api, "get_user", mock_get_user)
    monkeypatch.setattr(twitter_api, "get_follower_ids", value=[mock_data.get('follower_id'), ], raising=False)
    twitter_api_conn = TwitterApiConnector(twitter_api)
    return twitter_api_conn
