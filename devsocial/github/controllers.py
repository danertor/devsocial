# pylint: disable=too-few-public-methods, useless-super-delegation
# pylint: disable:too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
"""
Behaviour for the Twitter module.
"""
from devsocial.controllers.social_network import BaseDevSocialNet
from .models import GitHubDeveloper


# pylint: disable=too-few-public-methods, useless-super-delegation
class GitHubDevSocialNet(BaseDevSocialNet):
    def __init__(self):
        super().__init__()

    def connected(self, developer1: GitHubDeveloper, developer2: GitHubDeveloper):
        if developer1 != developer2:
            return bool(set(developer1.organizations) & set(developer2.organizations))
        return False
