# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
"""
Behaviour for the Twitter module.
"""
from .models import TwitterDeveloper
from ..controllers import BaseSocialController


# pylint: disable=too-few-public-methods, useless-super-delegation
class TwitterConnectedController(BaseSocialController):
    developer_type: type = TwitterDeveloper
    developer_type_name: type = TwitterDeveloper.__name__

    def __init__(self):
        super().__init__()

    @staticmethod
    def connected(developer1: TwitterDeveloper, developer2: TwitterDeveloper) -> bool:
        return developer1.id in developer2.followers and developer2.id in developer1.followers
