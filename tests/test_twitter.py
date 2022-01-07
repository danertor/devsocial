# pylint: disable=missing-module-docstring, missing-function-docstring, unused-variable
from devsocial.twitter.controllers import TwitterDevSocialNet
from devsocial.twitter.models import TwitterDeveloper


def test_twitter_dev_has_followers():
    followers = ([TwitterDeveloper(handle) for handle in ('homer', 'moe')])
    twitter_dev: TwitterDeveloper = TwitterDeveloper('krasty', followers=followers)
    assert followers[0] in twitter_dev.followers


def test_twitter_dev_has_no_followers():
    twitter_dev: TwitterDeveloper = TwitterDeveloper('krasty')
    assert not twitter_dev.followers


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
