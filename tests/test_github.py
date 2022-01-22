# pylint: disable=missing-module-docstring, disable=missing-class-docstring, missing-function-docstring
# pylint: disable=unused-variable, unused-argument, no-self-use

from unittest.mock import Mock
from typing import List
import pytest


from devsocial.github.models import GitHubDeveloper, GitHubOrganisation
from devsocial.github.controllers import GitHubConnectedController
from devsocial.github.connectors import GitHubApiType, GitHubApiConnector, create_api


def test_github_dev_belongs_organisation():
    organisations = [GitHubOrganisation(name) for name in ("Nuclear Plant", "Moe's Tavern")]
    github_dev: GitHubDeveloper = GitHubDeveloper('homer', organisations=organisations)
    assert organisations[0] in github_dev.organisations


def test_github_dev_belongs_no_organisation():
    github_dev: GitHubDeveloper = GitHubDeveloper('homer')
    assert not github_dev.organisations


def test_two_developers_are_github_connected():
    organisations = [GitHubOrganisation('Nuclear plant'), ]
    github_dev1: GitHubDeveloper = GitHubDeveloper('homer', organisations=organisations)
    github_dev2: GitHubDeveloper = GitHubDeveloper('mrburns', organisations=organisations)
    github_net: GitHubConnectedController = GitHubConnectedController()
    assert github_net.connected(github_dev1, github_dev2)


def test_two_developers_are_not_github_connected():
    dev1_organisations = [GitHubOrganisation('Nuclear plant')]
    dev2_organisations = [GitHubOrganisation('TV show')]
    github_dev1: GitHubDeveloper = GitHubDeveloper('homer', organisations=dev1_organisations)
    github_dev2: GitHubDeveloper = GitHubDeveloper('krasty', organisations=dev2_organisations)
    github_net: GitHubConnectedController = GitHubConnectedController()
    assert not github_net.connected(github_dev1, github_dev2)


def test_check_same_developer_github_connected():
    dev1_organisations = [GitHubOrganisation('Nuclear plant')]
    github_dev1: GitHubDeveloper = GitHubDeveloper('homer', organisations=dev1_organisations)
    github_net: GitHubConnectedController = GitHubConnectedController()
    assert not github_net.connected(github_dev1, github_dev1)


class TestGitHubConnector:
    handle = 'homer'
    organisation = GitHubOrganisation('Nuclear plant')

    @pytest.fixture
    def github_api(self) -> GitHubApiType:
        api = create_api()
        return api

    def mock_get_orgs(self) -> List[Mock]:
        mock_org = Mock()
        mock_org.login = self.organisation.name
        return [mock_org, ]

    def mock_get_user(self, _) -> Mock:
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
    organisation = GitHubOrganisation('python-sg')

    @pytest.fixture
    def github_api(self) -> GitHubApiType:
        api = create_api()
        return api

    def test_get_developers_orgs(self, github_api: GitHubApiType):
        github_connector = GitHubApiConnector(github_api)
        github_dev_organisations = github_connector.get_users_orgs(self.github_dev_handle)
        assert self.organisation in github_dev_organisations

    def test_get_user(self, github_api: GitHubApiType):
        github_connector = GitHubApiConnector(github_api)
        github_dev = github_connector.get_user(self.github_dev_handle)
        assert github_dev.handle == self.github_dev_handle
