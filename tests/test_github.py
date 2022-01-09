# pylint: disable=missing-module-docstring, disable=missing-class-docstring, missing-function-docstring
# pylint: disable=unused-variable, unused-argument, no-self-use

from unittest.mock import Mock
import github
import pytest

from devsocial.models.organization import Organization
from devsocial.github.models import GitHubDeveloper
from devsocial.github.controllers import GitHubConnectedController
from devsocial.github.connectors import GitHubApiConnector


def test_github_dev_belongs_organization():
    organizations = [Organization(name) for name in ("Nuclear Plant", "Moe's Tavern")]
    github_dev: GitHubDeveloper = GitHubDeveloper('homer', organizations=organizations)
    assert organizations[0] in github_dev.organizations


def test_github_dev_belongs_no_organization():
    github_dev: GitHubDeveloper = GitHubDeveloper('homer')
    assert not github_dev.organizations


def test_two_developers_are_github_connected():
    organizations = [Organization('Nuclear plant'), ]
    github_dev1: GitHubDeveloper = GitHubDeveloper('homer', organizations=organizations)
    github_dev2: GitHubDeveloper = GitHubDeveloper('mrburns', organizations=organizations)
    github_net: GitHubConnectedController = GitHubConnectedController()
    assert github_net.connected(github_dev1, github_dev2)


def test_two_developers_are_not_github_connected():
    dev1_organizations = [Organization('Nuclear plant')]
    dev2_organizations = [Organization('TV show')]
    github_dev1: GitHubDeveloper = GitHubDeveloper('homer', organizations=dev1_organizations)
    github_dev2: GitHubDeveloper = GitHubDeveloper('krasty', organizations=dev2_organizations)
    github_net: GitHubConnectedController = GitHubConnectedController()
    assert not github_net.connected(github_dev1, github_dev2)


def test_check_same_developer_github_connected():
    dev1_organizations = [Organization('Nuclear plant')]
    github_dev1: GitHubDeveloper = GitHubDeveloper('homer', organizations=dev1_organizations)
    github_net: GitHubConnectedController = GitHubConnectedController()
    assert not github_net.connected(github_dev1, github_dev1)


class TestGitHubConnector:
    handle = 'homer'
    organization = Organization('Nuclear plant')

    @pytest.fixture(scope="class")
    def github_api(self):
        api = github.Github()
        api.already_patch = False
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
