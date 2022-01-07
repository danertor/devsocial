# pylint: disable=too-few-public-methods, useless-super-delegation
# pylint: disable:too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
"""
Behaviour for the Twitter module.
"""
from devsocial.controllers.social_network import BaseDevSocialNet
from .models import TwitterDeveloper


class TwitterDevSocialNet(BaseDevSocialNet):
    def __init__(self):
        super().__init__()

    def connected(self, developer1: TwitterDeveloper, developer2: TwitterDeveloper):
        return developer1 in developer2.followers and developer2 in developer1.followers
