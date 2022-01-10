# pylint: disable=missing-module-docstring, disable=missing-class-docstring, missing-function-docstring
# pylint: disable=unused-variable, unused-argument, no-self-use

from unittest.mock import Mock
from github import Github
import pytest


from devsocial.github.models import GitHubDeveloper, GitHubOrganization
from devsocial.github.controllers import GitHubConnectedController
from devsocial.github.connectors import GitHubApiConnector, create_api


def test_github_dev_belongs_organization():
    organizations = [GitHubOrganization(name) for name in ("Nuclear Plant", "Moe's Tavern")]
    github_dev: GitHubDeveloper = GitHubDeveloper('homer', organizations=organizations)
    assert organizations[0] in github_dev.organizations


def test_github_dev_belongs_no_organization():
    github_dev: GitHubDeveloper = GitHubDeveloper('homer')
    assert not github_dev.organizations


def test_two_developers_are_github_connected():
    organizations = [GitHubOrganization('Nuclear plant'), ]
    github_dev1: GitHubDeveloper = GitHubDeveloper('homer', organizations=organizations)
    github_dev2: GitHubDeveloper = GitHubDeveloper('mrburns', organizations=organizations)
    github_net: GitHubConnectedController = GitHubConnectedController()
    assert github_net.connected(github_dev1, github_dev2)


def test_two_developers_are_not_github_connected():
    dev1_organizations = [GitHubOrganization('Nuclear plant')]
    dev2_organizations = [GitHubOrganization('TV show')]
    github_dev1: GitHubDeveloper = GitHubDeveloper('homer', organizations=dev1_organizations)
    github_dev2: GitHubDeveloper = GitHubDeveloper('krasty', organizations=dev2_organizations)
    github_net: GitHubConnectedController = GitHubConnectedController()
    assert not github_net.connected(github_dev1, github_dev2)


def test_check_same_developer_github_connected():
    dev1_organizations = [GitHubOrganization('Nuclear plant')]
    github_dev1: GitHubDeveloper = GitHubDeveloper('homer', organizations=dev1_organizations)
    github_net: GitHubConnectedController = GitHubConnectedController()
    assert not github_net.connected(github_dev1, github_dev1)


class TestGitHubConnector:
    handle = 'homer'
    organization = GitHubOrganization('Nuclear plant')

    @pytest.fixture
    def github_api(self):
        api = create_api()
        return api

    def mock_get_orgs(self):
        mock_org = Mock()
        mock_org.login = self.organization.name
        return [mock_org, ]

    def mock_get_user(self, _):
        mock_user = Mock()
        mock_user.get_orgs = self.mock_get_orgs
        return mock_user

    def test_get_user(self, monkeypatch, github_api):
        monkeypatch.setattr(github_api, "get_user", self.mock_get_user)
        github_connector = GitHubApiConnector(github_api)
        github_dev = github_connector.get_user(self.handle)
        assert github_dev.handle == self.handle


@pytest.mark.skip(reason="Disable external api communication")
class TestGitHubExternalApi:
    github_dev_handle = 'sfdye'
    organization = GitHubOrganization('python-sg')

    @pytest.fixture
    def github_api(self) -> Github:
        api = create_api()
        return api

    def test_get_developers_orgs(self, github_api: Github):
        github_connector = GitHubApiConnector(github_api)
        github_dev_organizations = github_connector.get_users_orgs(self.github_dev_handle)
        assert self.organization in github_dev_organizations

    def test_get_user(self, github_api: Github):
        github_connector = GitHubApiConnector(github_api)
        github_dev = github_connector.get_user(self.github_dev_handle)
        assert github_dev.handle == self.github_dev_handle
