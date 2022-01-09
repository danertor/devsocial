# pylint: disable=missing-module-docstring, disable=missing-class-docstring, missing-function-docstring
# pylint: disable=unused-variable, unused-argument

from devsocial.controllers.social_network import DevSocialNet
from devsocial.models.organization import Organization
from devsocial.models.social_developer import SocialDeveloper
from devsocial.github.models import GitHubDeveloper
from devsocial.twitter.models import TwitterDeveloper


def test_two_social_developers_are_connected():
    dev1_handle = 'homer'
    dev2_handle = 'lenny'
    organization = Organization("Nuclear Plant")

    twitter_dev1: TwitterDeveloper = TwitterDeveloper(dev1_handle)
    twitter_dev2: TwitterDeveloper = TwitterDeveloper(dev2_handle)
    twitter_dev1.followers.append(twitter_dev2)
    twitter_dev2.followers.append(twitter_dev1)

    github_dev1: GitHubDeveloper = GitHubDeveloper(dev1_handle)
    github_dev2: GitHubDeveloper = GitHubDeveloper(dev2_handle)
    github_dev1.organizations.append(organization)
    github_dev2.organizations.append(organization)

    dev1: SocialDeveloper = SocialDeveloper(dev1_handle)
    dev1.add_account(twitter_dev1)
    dev1.add_account(github_dev1)

    dev2: SocialDeveloper = SocialDeveloper(dev2_handle)
    dev2.add_account(twitter_dev2)
    dev2.add_account(github_dev2)

    social_net: DevSocialNet = DevSocialNet()
    assert social_net.connected(dev1, dev2)


def test_two_social_developers_are_not_fully_connected():
    dev1_handle = 'homer'
    dev2_handle = 'flanders'
    organization = Organization("Evergreen Terrace St.")

    twitter_dev1: TwitterDeveloper = TwitterDeveloper(dev1_handle)
    twitter_dev2: TwitterDeveloper = TwitterDeveloper(dev2_handle)

    twitter_dev1.followers.append(twitter_dev2)

    github_dev1: GitHubDeveloper = GitHubDeveloper(dev1_handle)
    github_dev2: GitHubDeveloper = GitHubDeveloper(dev2_handle)
    github_dev1.organizations.append(organization)
    github_dev2.organizations.append(organization)

    dev1: SocialDeveloper = SocialDeveloper(dev1_handle)
    dev1.add_account(twitter_dev1)
    dev1.add_account(github_dev1)

    dev2: SocialDeveloper = SocialDeveloper(dev2_handle)
    dev2.add_account(twitter_dev2)
    dev2.add_account(github_dev2)

    social_net: DevSocialNet = DevSocialNet()
    assert not social_net.connected(dev1, dev2)
