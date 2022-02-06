# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
# pylint: disable=unused-variable, unused-argument, too-few-public-methods, unused-import, no-self-use
import pytest
from flask.testing import FlaskClient

from devsocial.config import get_os_var
from devsocial.dbmodels import db, migrate
from devsocial.exceptions import InvalidHandleError
from devsocial.service.app import app
from devsocial.service.v1.routes import dev_social_api
from devsocial.service.v1.handlers import register
import devsocial.service.routes
from devsocial.github.models import GitHubDeveloper, GitHubOrganisation
from devsocial.twitter.models import TwitterDeveloper


# pylint: disable=redefined-outer-name
from tests.utils import remove_registered_at


@pytest.fixture(scope='module')
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config["DEBUG"] = get_os_var('FLASK_DEBUG', default='False', mandatory=False) == 'True'
    app.config["Development"] = app.config["DEBUG"]
    app.config["LOG_LEVEL"] = "DEBUG" if app.config["DEBUG"] else 'ERROR'
    app.register_blueprint(dev_social_api, url_prefix='/')

    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)
            migrate.init_app(app, db)
        yield client


SERVICE_API_PORT = '8080'
SERVICE_API_HOST = 'localhost'


# pylint: disable=invalid-name
class TestRealtimeApi:
    realtime_endpoint = f"http://{SERVICE_API_HOST}:SERVICE_API_PORT"
    realtime_uri = "connected/realtime/{}/{}"
    registered_at = "2022-01-25T17:55:10Z"

    # Two connected developers
    dev1_handle = 'homer'
    dev2_handle = 'lenny'
    dev1_twitter_id = '1'
    dev2_twitter_id = '2'
    twitter_dev1: TwitterDeveloper = TwitterDeveloper(dev1_handle, id=dev1_twitter_id)
    twitter_dev2: TwitterDeveloper = TwitterDeveloper(dev2_handle, id=dev2_twitter_id)
    twitter_dev1.followers.append(twitter_dev2.id)
    twitter_dev2.followers.append(twitter_dev1.id)

    organisation_name_connected = "Nuclear Plant"
    organisation = GitHubOrganisation(organisation_name_connected)
    github_dev1: GitHubDeveloper = GitHubDeveloper(dev1_handle)
    github_dev1.organisations.append(organisation)
    github_dev2: GitHubDeveloper = GitHubDeveloper(dev2_handle)
    github_dev2.organisations.append(organisation)

    twitter_devs_connected = [twitter_dev1, twitter_dev2]
    github_devs_connected = [github_dev1, github_dev2]
    twitter_devs_connected_iter = (i for i in range(len(twitter_devs_connected)))
    github_devs_connected_iter = (i for i in range(len(github_devs_connected)))

    # Two not fully connected developers
    dev3_handle = 'krasty'
    dev4_handle = 'bart'
    dev3_twitter_id = '3'
    dev4_twitter_id = '4'
    twitter_dev3: TwitterDeveloper = TwitterDeveloper(dev3_handle, id=dev3_twitter_id)
    twitter_dev4: TwitterDeveloper = TwitterDeveloper(dev4_handle, id=dev4_twitter_id)
    twitter_dev3.followers.append(twitter_dev4.id)

    organisation_name_dev3 = "TV Show"
    organisation = GitHubOrganisation(organisation_name_connected)
    github_dev3: GitHubDeveloper = GitHubDeveloper(dev3_handle)
    github_dev3.organisations.append(organisation)
    github_dev4: GitHubDeveloper = GitHubDeveloper(dev4_handle)

    twitter_devs_not_connected = [twitter_dev3, twitter_dev4]
    github_devs_not_connected = [github_dev3, github_dev4]
    twitter_devs_not_connected_iter = (i for i in range(len(twitter_devs_not_connected)))
    github_devs_not_connected_iter = (i for i in range(len(github_devs_not_connected)))

    def mock_twitter_get_user_connected(self, *ignored_arg):
        try:
            idx = next(self.twitter_devs_connected_iter)
        except StopIteration as _:
            self.twitter_devs_connected_iter = (i for i in range(len(self.twitter_devs_connected)))
            idx = next(self.twitter_devs_connected_iter)
        return self.twitter_devs_connected[idx]

    def mock_github_user_user_connected(self, *ignored_arg):
        try:
            idx = next(self.github_devs_connected_iter)
        except StopIteration as _:
            self.github_devs_connected_iter = (i for i in range(len(self.github_devs_connected)))
            idx = next(self.github_devs_connected_iter)
        return self.github_devs_connected[idx]

    def mock_twitter_get_user_not_connected(self, *ignored_arg):
        try:
            idx = next(self.twitter_devs_not_connected_iter)
        except StopIteration as _:
            self.twitter_devs_not_connected_iter = (i for i in range(len(self.twitter_devs_not_connected)))
            idx = next(self.twitter_devs_not_connected_iter)
        return self.twitter_devs_not_connected[idx]

    def mock_github_user_user_not_connected(self, *ignored_arg):
        try:
            idx = next(self.github_devs_not_connected_iter)
        except StopIteration as _:
            self.github_devs_not_connected_iter = (i for i in range(len(self.github_devs_not_connected)))
            idx = next(self.github_devs_not_connected_iter)
        return self.github_devs_not_connected[idx]

    def mock_twitter_get_user_not_found(self, handle, *ignored_arg):
        raise InvalidHandleError(f"{handle} is no a valid user in twitter")

    def mock_github_get_user_not_found(self, handle, *ignored_arg):
        raise InvalidHandleError(f"{handle} is no a valid user in github")

    def test_realtime_response_200_ok_connected(self, monkeypatch, client: FlaskClient):
        expected_response = {'connected': True, 'organisations': [self.organisation_name_connected]}
        with monkeypatch.context() as mp:
            mp.setattr(devsocial.service.v1.social_net.twitter_connector,
                       "get_user", self.mock_twitter_get_user_connected)
            mp.setattr(devsocial.service.v1.social_net.github_connector,
                       "get_user", self.mock_github_user_user_connected)
            response = client.get(self.realtime_uri.format(self.dev1_handle, self.dev2_handle))
        assert response.status_code == 200
        assert response.json == expected_response

    def test_realtime_response_200_ok_not_connected(self, monkeypatch, client: FlaskClient):
        expected_response = {'connected': False}
        with monkeypatch.context() as mp:
            mp.setattr(devsocial.service.v1.social_net.twitter_connector,
                       "get_user", self.mock_twitter_get_user_not_connected)
            mp.setattr(devsocial.service.v1.social_net.github_connector,
                       "get_user", self.mock_github_user_user_not_connected)
            response = client.get(self.realtime_uri.format(self.dev3_handle, self.dev4_handle))
        assert response.status_code == 200
        assert response.json == expected_response

    def test_realtime_response_400_bad_same_handle(self, monkeypatch, client: FlaskClient):
        expected_response = {'errors': ["'handle1' and 'handle2' have the same value", ]}
        with monkeypatch.context() as mp:
            mp.setattr(devsocial.service.v1.social_net.twitter_connector,
                       "get_user", self.mock_twitter_get_user_connected)
            mp.setattr(devsocial.service.v1.social_net.github_connector,
                       "get_user", self.mock_github_user_user_connected)
            response = client.get(self.realtime_uri.format(self.dev1_handle, self.dev1_handle))
        assert response.status_code == 400
        assert response.json == expected_response

    def test_realtime_response_404_handle_not_found(self, monkeypatch, client: FlaskClient):
        expected_response = {'errors': [f"{self.dev1_handle} is no a valid user in github",
                                        f"{self.dev1_handle} is no a valid user in twitter",
                                        f"{self.dev2_handle} is no a valid user in github",
                                        f"{self.dev2_handle} is no a valid user in twitter"]}
        with monkeypatch.context() as mp:
            mp.setattr(devsocial.service.v1.social_net.twitter_connector,
                       "get_user", self.mock_twitter_get_user_not_found)
            mp.setattr(devsocial.service.v1.social_net.github_connector,
                       "get_user", self.mock_github_get_user_not_found)
            response = client.get(self.realtime_uri.format(self.dev1_handle, self.dev2_handle))
        assert response.status_code == 404
        assert response.json == expected_response


# pylint: disable=invalid-name
class TestRegisterApi:
    realtime_endpoint = f"http://{SERVICE_API_HOST}:SERVICE_API_PORT"
    realtime_uri = "connected/realtime/{}/{}"
    registered_at = "2022-01-25T17:55:10Z"

    # Two connected developers
    dev1_handle = 'homer'
    dev2_handle = 'lenny'
    dev1_twitter_id = '1'
    dev2_twitter_id = '2'
    twitter_dev1: TwitterDeveloper = TwitterDeveloper(dev1_handle, id=dev1_twitter_id)
    twitter_dev2: TwitterDeveloper = TwitterDeveloper(dev2_handle, id=dev2_twitter_id)
    twitter_dev1.followers.append(twitter_dev2.id)
    twitter_dev2.followers.append(twitter_dev1.id)

    organisation_name_connected = "Nuclear Plant"
    organisation = GitHubOrganisation(organisation_name_connected)
    github_dev1: GitHubDeveloper = GitHubDeveloper(dev1_handle)
    github_dev1.organisations.append(organisation)
    github_dev2: GitHubDeveloper = GitHubDeveloper(dev2_handle)
    github_dev2.organisations.append(organisation)

    twitter_devs_connected = [twitter_dev1, twitter_dev2]
    github_devs_connected = [github_dev1, github_dev2]
    twitter_devs_connected_iter = (i for i in range(len(twitter_devs_connected)))
    github_devs_connected_iter = (i for i in range(len(github_devs_connected)))

    # Two not fully connected developers
    dev3_handle = 'krasty'
    dev4_handle = 'bart'
    dev3_twitter_id = '3'
    dev4_twitter_id = '4'
    twitter_dev3: TwitterDeveloper = TwitterDeveloper(dev3_handle, id=dev3_twitter_id)
    twitter_dev4: TwitterDeveloper = TwitterDeveloper(dev4_handle, id=dev4_twitter_id)
    twitter_dev3.followers.append(twitter_dev4.id)

    organisation_name_dev3 = "TV Show"
    organisation = GitHubOrganisation(organisation_name_connected)
    github_dev3: GitHubDeveloper = GitHubDeveloper(dev3_handle)
    github_dev3.organisations.append(organisation)
    github_dev4: GitHubDeveloper = GitHubDeveloper(dev4_handle)

    twitter_devs_not_connected = [twitter_dev3, twitter_dev4]
    github_devs_not_connected = [github_dev3, github_dev4]
    twitter_devs_not_connected_iter = (i for i in range(len(twitter_devs_not_connected)))
    github_devs_not_connected_iter = (i for i in range(len(github_devs_not_connected)))


    @pytest.fixture(scope='function')
    def reset_db(self):
        db.drop_all()
        db.create_all()

    def mock_twitter_get_user_connected(self, *ignored_arg):
        try:
            idx = next(self.twitter_devs_connected_iter)
        except StopIteration as _:
            self.twitter_devs_connected_iter = (i for i in range(len(self.twitter_devs_connected)))
            idx = next(self.twitter_devs_connected_iter)
        return self.twitter_devs_connected[idx]

    def mock_github_user_user_connected(self, *ignored_arg):
        try:
            idx = next(self.github_devs_connected_iter)
        except StopIteration as _:
            self.github_devs_connected_iter = (i for i in range(len(self.github_devs_connected)))
            idx = next(self.github_devs_connected_iter)
        return self.github_devs_connected[idx]

    def mock_twitter_get_user_not_connected(self, *ignored_arg):
        try:
            idx = next(self.twitter_devs_not_connected_iter)
        except StopIteration as _:
            self.twitter_devs_not_connected_iter = (i for i in range(len(self.twitter_devs_not_connected)))
            idx = next(self.twitter_devs_not_connected_iter)
        return self.twitter_devs_not_connected[idx]

    def mock_github_user_user_not_connected(self, *ignored_arg):
        try:
            idx = next(self.github_devs_not_connected_iter)
        except StopIteration as _:
            self.github_devs_not_connected_iter = (i for i in range(len(self.github_devs_not_connected)))
            idx = next(self.github_devs_not_connected_iter)
        return self.github_devs_not_connected[idx]

    def mock_twitter_get_user_not_found(self, handle, *ignored_arg):
        raise InvalidHandleError(f"{handle} is no a valid user in twitter")

    def mock_github_get_user_not_found(self, handle, *ignored_arg):
        raise InvalidHandleError(f"{handle} is no a valid user in github")

    def test_register_response_200_ok_connected(self, monkeypatch, client: FlaskClient, reset_db: None):
        expected_response = [{'connected': True,
                              'organisations': ['Nuclear Plant'],
                              'registered_at': '2022-02-06T13:18:37Z'}]
        with monkeypatch.context() as mp:
            mp.setattr(devsocial.service.v1.social_net.twitter_connector,
                       "get_user", self.mock_twitter_get_user_connected)
            mp.setattr(devsocial.service.v1.social_net.github_connector,
                       "get_user", self.mock_github_user_user_connected)
            _ = client.get(self.realtime_uri.format(self.dev1_handle, self.dev2_handle))
            response = register(self.dev1_handle, self.dev2_handle)

        response_cleaned = remove_registered_at(response.json)
        expected_response_cleaned = remove_registered_at(expected_response)
        assert response.status_code == 200
        assert response_cleaned == expected_response_cleaned

    def test_realtime_response_200_ok_not_connected(self, monkeypatch, client: FlaskClient):
        expected_response = [{'connected': False, 'registered_at': '2022-02-06T13:18:37Z'}]
        with monkeypatch.context() as mp:
            mp.setattr(devsocial.service.v1.social_net.twitter_connector,
                       "get_user", self.mock_twitter_get_user_not_connected)
            mp.setattr(devsocial.service.v1.social_net.github_connector,
                       "get_user", self.mock_github_user_user_not_connected)
            _ = client.get(self.realtime_uri.format(self.dev3_handle, self.dev4_handle))
            response = register(self.dev3_handle, self.dev4_handle)

        response_cleaned = remove_registered_at(response.json)
        expected_response_cleaned = remove_registered_at(expected_response)
        assert response.status_code == 200
        assert response_cleaned == expected_response_cleaned
