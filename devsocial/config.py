# pylint: disable=missing-module-docstring, disable=missing-function-docstring
import os

from devsocial.twitter.controllers import TwitterConnectedController
from devsocial.github.controllers import GitHubConnectedController


def get_os_var(var_name: str, default: str = None, mandatory: bool = True) -> None:
    value = os.environ.get(var_name)
    if not value and mandatory:
        raise ValueError(f"The environment variable {var_name} is not set.")
    if not value and default:
        return default
    return value


FULLY_CONNECTED_CONTROLLERS = (TwitterConnectedController, GitHubConnectedController)
FULLY_CONNECTED_DEVELOPER_TYPES = [controller.developer_type for controller in FULLY_CONNECTED_CONTROLLERS]
FULLY_CONNECTED_DEVELOPER_TYPE_NAMES = [cls.__name__ for cls in FULLY_CONNECTED_DEVELOPER_TYPES]


TWITTER_API = {
    "MAX_RESULTS": 100,
    "CONSUMER_KEY": get_os_var('TWITTER_API_CONSUMER_KEY'),
    "CONSUMER_SECRET": get_os_var('TWITTER_API_CONSUMER_SECRET'),
    "ACCESS_TOKEN": get_os_var('TWITTER_API_ACCESS_TOKEN'),
    "ACCESS_TOKEN_SECRET": get_os_var('TWITTER_API_ACCESS_TOKEN_SECRET')
}


GITHUB_API = {
    "TOKEN": get_os_var('GITHUB_API_TOKEN')
}
