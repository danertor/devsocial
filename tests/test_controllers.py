# pylint: disable=missing-module-docstring, disable=missing-class-docstring, missing-function-docstring
# pylint: disable=unused-variable, unused-argument, too-few-public-methods
from collections import defaultdict
from unittest.mock import Mock
from typing import List
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pytest

from devsocial.controllers.dbhistory import DBHistoryController
from devsocial.models.base_developer import HandleType
from devsocial.models.social_developer import SocialDeveloper
from devsocial.controllers.social_network import DevSocialNet
from devsocial.github.models import GitHubDeveloper, GitHubOrganisation
from devsocial.github.connectors import GitHubApiType
from devsocial.github.connectors import create_api as create_github_api
from devsocial.models.social_network import \
    DeveloperConnectionStatusOk, \
    DeveloperConnectionStatus, \
    DeveloperConnectionStatusFalse, \
    DeveloperHistoryConnectionStatusFalse, \
    DeveloperHistoryConnectionStatusOk, \
    DeveloperConnectionStatusSameHandleError
from devsocial.twitter.connectors import TwitterApiType
from devsocial.twitter.connectors import create_api as create_twitter_api
from devsocial.twitter.models import TwitterDeveloper, TwitterDeveloperIdType
from devsocial.service.app import create_app
from devsocial.dbmodels import db


def test_two_social_developers_are_connected():
    dev1_handle = 'homer'
    dev2_handle = 'lenny'
    organisation = GitHubOrganisation("Nuclear Plant")

    twitter_dev1: TwitterDeveloper = TwitterDeveloper(dev1_handle, id='1')
    twitter_dev2: TwitterDeveloper = TwitterDeveloper(dev2_handle, id='2')
    twitter_dev1.followers.append(twitter_dev2.id)
    twitter_dev2.followers.append(twitter_dev1.id)

    github_dev1: GitHubDeveloper = GitHubDeveloper(dev1_handle)
    github_dev2: GitHubDeveloper = GitHubDeveloper(dev2_handle)
    github_dev1.organisations.append(organisation)
    github_dev2.organisations.append(organisation)

    dev1: SocialDeveloper = SocialDeveloper(dev1_handle)
    dev1.add_account(twitter_dev1)
    dev1.add_account(github_dev1)

    dev2: SocialDeveloper = SocialDeveloper(dev2_handle)
    dev2.add_account(twitter_dev2)
    dev2.add_account(github_dev2)

    social_net: DevSocialNet = DevSocialNet()
    assert social_net.developers_connected(dev1, dev2)


def test_two_social_developers_are_not_fully_connected():
    dev1_handle = 'homer'
    dev2_handle = 'flanders'
    organisation = GitHubOrganisation("Evergreen Terrace St.")

    twitter_dev1: TwitterDeveloper = TwitterDeveloper(dev1_handle, id='1')
    twitter_dev2: TwitterDeveloper = TwitterDeveloper(dev2_handle, id='2')

    twitter_dev1.followers.append(twitter_dev2.id)

    github_dev1: GitHubDeveloper = GitHubDeveloper(dev1_handle)
    github_dev2: GitHubDeveloper = GitHubDeveloper(dev2_handle)
    github_dev1.organisations.append(organisation)
    github_dev2.organisations.append(organisation)

    dev1: SocialDeveloper = SocialDeveloper(dev1_handle)
    dev1.add_account(twitter_dev1)
    dev1.add_account(github_dev1)

    dev2: SocialDeveloper = SocialDeveloper(dev2_handle)
    dev2.add_account(twitter_dev2)
    dev2.add_account(github_dev2)

    social_net: DevSocialNet = DevSocialNet()
    assert not social_net.developers_connected(dev1, dev2)


def test_error_response_handles_connected_same_handle():
    same_handle = 'sideshow_bob'
    social_net: DevSocialNet = DevSocialNet()
    response = social_net.handles_connected(same_handle, same_handle)
    assert isinstance(response, DeveloperConnectionStatusSameHandleError)


class TestTwoHandlesAreConnected:
    registered_at = "2022-01-25T17:55:10Z"
    dev1_handle = 'homer'
    dev2_handle = 'lenny'
    dev1_twitter_id = 1
    dev2_twitter_id = 2
    organisation_names = ("Nuclear Plant", "Moe's Tavern")
    organisations = [GitHubOrganisation(name) for name in organisation_names]
    twitter_dev_ids = (id for id in (dev1_twitter_id, dev2_twitter_id))
    twitter_followers_ids = (id for id in (dev2_twitter_id, dev1_twitter_id))

    @pytest.fixture
    def twitter_api(self, monkeypatch) -> TwitterApiType:
        twitter_api = create_twitter_api()
        monkeypatch.setattr(twitter_api, "get_user", self.mock_twitter_get_user)
        monkeypatch.setattr(twitter_api, "get_follower_ids", self.mock_twitter_get_follower_ids, raising=False)
        return twitter_api

    def mock_twitter_get_user(self, screen_name: str, *args, **kwargs) -> Mock:
        mock_follower_response = Mock()
        mock_follower_response.id_str = next(self.twitter_dev_ids)
        return mock_follower_response

    def mock_twitter_get_follower_ids(self, screen_name: str, *args, **kwargs) -> TwitterDeveloperIdType:
        return [next(self.twitter_followers_ids), ]

    @pytest.fixture
    def github_api(self, monkeypatch) -> GitHubApiType:
        github_api = create_github_api()
        monkeypatch.setattr(github_api, "get_user", self.mock_github_get_user)
        return github_api

    def mock_github_get_orgs(self) -> List[Mock]:
        mock_organisations = []
        for org_name in self.organisation_names:
            mock_org = Mock()
            mock_org.login = org_name
            mock_organisations.append(mock_org)
        return mock_organisations

    def mock_github_get_user(self, _) -> Mock:
        mock_user = Mock()
        mock_user.get_orgs = self.mock_github_get_orgs
        return mock_user

    def test_two_handles_are_connected(self, twitter_api: TwitterApiType, github_api: GitHubApiType):
        social_net: DevSocialNet = DevSocialNet(twitter_api, github_api)
        result: DeveloperConnectionStatus = social_net.handles_connected(self.dev1_handle, self.dev2_handle)
        expected: DeveloperConnectionStatusOk = DeveloperConnectionStatusOk(result.registered_at,
                                                                            self.dev1_handle,
                                                                            self.dev2_handle,
                                                                            organisations=self.organisations)
        assert result == expected


class TestDBHistoryController:
    registered_at = "2022-01-25T17:55:10Z"
    dev1_handle = 'homer'
    dev2_handle = 'lenny'
    organisation_names = ("Nuclear Plant", "Moe's Tavern")
    organisations = [GitHubOrganisation(name) for name in organisation_names]
    dev_conn_status_first = DeveloperConnectionStatusFalse(registered_at, dev1_handle, dev2_handle)
    dev_conn_status_last = DeveloperConnectionStatusOk(registered_at,
                                                       dev1_handle,
                                                       dev2_handle,
                                                       organisations=organisations)
    dev_history_conn_status_first = DeveloperHistoryConnectionStatusFalse(registered_at)
    dev_history_conn_status_last = DeveloperHistoryConnectionStatusOk(registered_at, organisations=organisations)

    @staticmethod
    @pytest.fixture
    def mock_db() -> Mock:
        class MockDBSession:
            def __init__(self):
                self.history = defaultdict(list)

            def add(self, dev_conn_status: DeveloperConnectionStatus) -> None:
                self.history[f"{dev_conn_status.handle1}_{dev_conn_status.handle2}"].append(dev_conn_status)

            def query(self, handle1: HandleType, handle2: HandleType) -> List[DeveloperConnectionStatus]:
                return self.history[f"{handle1}_{handle2}"]

            def commit(self):
                pass
        local_db = Mock()
        session = MockDBSession()
        local_db.session = session
        return local_db


    @staticmethod
    @pytest.fixture
    def app() -> Flask:
        return create_app()

    @staticmethod
    @pytest.fixture
    def local_db(app: Flask) -> Mock:
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        db.init_app(app)
        return db

    def test_save_connection_history_in_db(self, local_db: SQLAlchemy, app: Flask):
        with app.app_context():
            db_history_controller = DBHistoryController(local_db)
            local_db.create_all()
            db_history_controller.save_dev_connection(self.dev_conn_status_first)
            db_history_controller.save_dev_connection(self.dev_conn_status_last)
            db_results = db_history_controller.get_dev_connections(self.dev1_handle, self.dev2_handle)

        assert db_results[0] == self.dev_history_conn_status_first
        assert db_results[1] == self.dev_history_conn_status_last
