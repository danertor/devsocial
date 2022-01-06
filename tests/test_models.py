# pylint: disable=missing-module-docstring, missing-function-docstring, unused-variable
import pytest
from devsocial.models.developer import BaseDeveloper, GitHubDeveloper, TwitterDeveloper, HandleType
from devsocial.models.organization import Organization


def test_create_developer():
    dev: BaseDeveloper = BaseDeveloper('homer')
    assert dev


# pylint: disable=no-value-for-parameter
def test_fail_developer_with_no_handle():
    with pytest.raises(TypeError):
        empty_dev: BaseDeveloper = BaseDeveloper()


def test_developers_equal():
    dev1: BaseDeveloper = BaseDeveloper('homer')
    dev2: BaseDeveloper = BaseDeveloper('homer')
    assert dev1 == dev2


def test_developers_not_equal():
    dev1: BaseDeveloper = BaseDeveloper('homer')
    dev2: BaseDeveloper = BaseDeveloper('krusty')
    assert dev1 != dev2

    with pytest.raises(AssertionError):
        assert dev1.handle == dev2.handle


def test_github_dev_belongs_organization():
    organizations = [Organization(name) for name in ("Nuclear Plant", "Moe's Tavern")]
    github_dev: GitHubDeveloper = GitHubDeveloper('homer', organizations=organizations)
    assert organizations[0] in github_dev.organizations


def test_github_dev_belongs_no_organization():
    github_dev: GitHubDeveloper = GitHubDeveloper('homer')
    assert not github_dev.organizations


def test_twitter_dev_has_followers():
    followers = ([HandleType(handle) for handle in ('homer', 'moe')])
    twitter_dev: TwitterDeveloper = TwitterDeveloper('krasty', followers=followers)
    assert followers[0] in twitter_dev.followers


def test_twitter_dev_has_no_followers():
    twitter_dev: TwitterDeveloper = TwitterDeveloper('krasty')
    assert not twitter_dev.followers
