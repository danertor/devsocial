# pylint: disable=missing-module-docstring, missing-function-docstring, unused-variable
from devsocial.models.organization import Organization
from devsocial.github.models import GitHubDeveloper
from devsocial.github.controllers import GitHubDevSocialNet


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
    github_net: GitHubDevSocialNet = GitHubDevSocialNet()
    assert github_net.connected(github_dev1, github_dev2)


def test_two_developers_are_not_github_connected():
    dev1_organizations = [Organization('Nuclear plant')]
    dev2_organizations = [Organization('TV show')]
    github_dev1: GitHubDeveloper = GitHubDeveloper('homer', organizations=dev1_organizations)
    github_dev2: GitHubDeveloper = GitHubDeveloper('krasty', organizations=dev2_organizations)
    github_net: GitHubDevSocialNet = GitHubDevSocialNet()
    assert not github_net.connected(github_dev1, github_dev2)


def test_check_same_developer_github_connected():
    dev1_organizations = [Organization('Nuclear plant')]
    github_dev1: GitHubDeveloper = GitHubDeveloper('homer', organizations=dev1_organizations)
    github_net: GitHubDevSocialNet = GitHubDevSocialNet()
    assert not github_net.connected(github_dev1, github_dev1)
