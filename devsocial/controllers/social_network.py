# pylint disable:too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
"""
Each social network will have a the business logic implemented in this module.
Note: Please implement the base class methods listed below if you want to create you own social network controller.
"""
from abc import abstractmethod
from devsocial.models.developer import GitHubDeveloper, BaseDeveloper, TwitterDeveloper


# pylint: disable=too-few-public-methods
class BaseDevSocialNet:
    def __init__(self):
        pass

    @abstractmethod
    def connected(self, developer1: BaseDeveloper, developer2: BaseDeveloper):
        pass


# pylint: disable=too-few-public-methods, useless-super-delegation
class GitHubDevSocialNet(BaseDevSocialNet):
    def __init__(self):
        super().__init__()

    def connected(self, developer1: GitHubDeveloper, developer2: GitHubDeveloper):
        if developer1 != developer2:
            return bool(set(developer1.organizations) & set(developer2.organizations))
        return False


# pylint: disable=too-few-public-methods, useless-super-delegation
class TwitterDevSocialNet(BaseDevSocialNet):
    def __init__(self):
        super().__init__()

    def connected(self, developer1: TwitterDeveloper, developer2: TwitterDeveloper):
        return developer1 in developer2.followers and developer2 in developer1.followers
