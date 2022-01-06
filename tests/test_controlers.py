# pylint: disable=missing-module-docstring, missing-function-docstring, unused-variable
from devsocial.controllers.social_network import GitHubDevSocialNet, TwitterDevSocialNet
from devsocial.models.developer import GitHubDeveloper, TwitterDeveloper
from devsocial.models.organization import Organization


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


def test_two_developers_are_twitter_connected():
    twitter_dev1: TwitterDeveloper = TwitterDeveloper('homer')
    twitter_dev2: TwitterDeveloper = TwitterDeveloper('mrburns')
    twitter_dev1.followers.append(twitter_dev2)
    twitter_dev2.followers.append(twitter_dev1)
    twitter_net: TwitterDevSocialNet = TwitterDevSocialNet()
    assert twitter_net.connected(twitter_dev1, twitter_dev2)


def test_two_developers_are_not_twitter_connected():
    twitter_dev1: TwitterDeveloper = TwitterDeveloper('homer')
    twitter_dev2: TwitterDeveloper = TwitterDeveloper('flanders')
    twitter_dev2.followers.append(twitter_dev1)
    twitter_net: TwitterDevSocialNet = TwitterDevSocialNet()
    assert not twitter_net.connected(twitter_dev1, twitter_dev2)


def test_check_same_developer_twitter_connected():
    twitter_dev1: TwitterDeveloper = TwitterDeveloper('homer')
    twitter_net: TwitterDevSocialNet = TwitterDevSocialNet()
    assert not twitter_net.connected(twitter_dev1, twitter_dev1)


def test_check_same_developer_github_connected():
    dev1_organizations = [Organization('Nuclear plant')]
    github_dev1: GitHubDeveloper = GitHubDeveloper('homer', organizations=dev1_organizations)
    github_net: GitHubDevSocialNet = GitHubDevSocialNet()
    assert not github_net.connected(github_dev1, github_dev1)
