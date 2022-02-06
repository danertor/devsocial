# pylint: disable=too-few-public-methods, useless-super-delegation
# pylint: disable:too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
"""
Behaviour for the Twitter module.
"""
from .models import GitHubDeveloper
from ..controllers import BaseSocialController


# pylint: disable=too-few-public-methods, useless-super-delegation
class GitHubConnectedController(BaseSocialController):
    developer_type: type = GitHubDeveloper
    developer_type_name: type = GitHubDeveloper.__name__

    def __init__(self):
        super().__init__()

    @staticmethod
    def connected(developer1: GitHubDeveloper, developer2: GitHubDeveloper) -> bool:
        if developer1 != developer2:
            return bool(set(developer1.organisations) & set(developer2.organisations))
        return False
