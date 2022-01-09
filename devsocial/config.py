# pylint: disable=missing-module-docstring

import os
import json

from devsocial.twitter.controllers import TwitterConnectedController
from devsocial.github.controllers import GitHubConnectedController


FULLY_CONNECTED_CONTROLLERS = (TwitterConnectedController, GitHubConnectedController)
FULLY_CONNECTED_DEVELOPER_TYPES = [controller.developer_type for controller in FULLY_CONNECTED_CONTROLLERS]
FULLY_CONNECTED_DEVELOPER_TYPE_NAMES = [cls.__name__ for cls in FULLY_CONNECTED_DEVELOPER_TYPES]


local_config_path = os.environ.get('APPSETTINGS_PATH')
if local_config_path and os.path.isfile(local_config_path):
    with open(local_config_path, 'r', encoding='ANSI') as fin:
        local_config = json.load(fin)
else:
    local_config = {}


TWITTER_API = {
    "MAX_RESULTS": 100,
    "CONSUMER_KEY": "",
    "CONSUMER_SECRET": "",
    "ACCESS_TOKEN": "",
    "ACCESS_TOKEN_SECRET": ""
}

TWITTER_API = {**TWITTER_API, **local_config.get('TWITTER_API', {})}

GITHUB_API = {
    "TOKEN": ""
}

GITHUB_API = {**GITHUB_API, **local_config.get('GITHUB_API', {})}
