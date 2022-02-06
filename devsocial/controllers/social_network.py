"""
The service that contains the functionalities of the social network.
It integrates all of the parts of the applications.
"""
# pylint: disable:too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from typing import List, Union
from datetime import datetime

from devsocial import config
from devsocial.exceptions import InvalidHandleError
from devsocial.models.base_developer import HandleType
from devsocial.models.social_developer import SocialDeveloper
from devsocial.models.social_network import (
    DeveloperConnectionStatusOk,
    DeveloperConnectionStatusFalse,
    DeveloperConnectionStatusNotFound,
    DeveloperConnectionStatusSameHandleError
)
from devsocial.twitter.connectors import TwitterApiConnector, TwitterApiType
from devsocial.github.models import GitHubDeveloper, GitHubOrganisation
from devsocial.github.connectors import GitHubApiConnector, GitHubApiType
from devsocial.twitter.models import TwitterDeveloper


HandlesConnectedStatusTypes = Union[DeveloperConnectionStatusSameHandleError,
                                    DeveloperConnectionStatusNotFound,
                                    DeveloperConnectionStatusOk,
                                    DeveloperConnectionStatusFalse
                                    ]


class DevSocialNet:
    def __init__(self, twitter_api: TwitterApiType = None, github_api: GitHubApiType = None):
        super().__init__()
        self._social_controllers: list = [controller() for controller in config.FULLY_CONNECTED_CONTROLLERS]
        self.twitter_connector = TwitterApiConnector(twitter_api)
        self.github_connector = GitHubApiConnector(github_api)

    def developers_connected(self, developer1: SocialDeveloper, developer2: SocialDeveloper) -> bool:
        social_connections: List[bool] = []
        for social_controller in self._social_controllers:
            if not developer1.has_account_type(social_controller.developer_type) \
                    or not developer2.has_account_type(social_controller.developer_type):
                return False

            developer1_account = developer1.accounts[social_controller.developer_type_name]
            developer2_account = developer2.accounts[social_controller.developer_type_name]
            social_connections.append(social_controller.connected(developer1_account, developer2_account))
        return all(social_connections)

    def handles_connected(self, handle1: HandleType, handle2: HandleType) -> HandlesConnectedStatusTypes:
        if handle1 == handle2:
            return DeveloperConnectionStatusSameHandleError(handle1)

        errors: list = []
        twitter_devs: List[TwitterDeveloper] = []
        github_devs: List[GitHubDeveloper] = []
        for twitter_handle in (handle1, handle2):
            try:
                twitter_devs.append(self.twitter_connector.get_user(twitter_handle))
            except InvalidHandleError as handle_error:
                errors.append(str(handle_error))

        for github_handle in (handle1, handle2):
            try:
                github_devs.append(self.github_connector.get_user(github_handle))
            except InvalidHandleError as handle_error:
                errors.append(str(handle_error))

        if errors:
            return DeveloperConnectionStatusNotFound(errors)

        social_dev1 = SocialDeveloper(handle1)
        social_dev1.add_account(twitter_devs[0])
        social_dev1.add_account(github_devs[0])

        social_dev2 = SocialDeveloper(handle2)
        social_dev2.add_account(twitter_devs[1])
        social_dev2.add_account(github_devs[1])

        connected_status = self.developers_connected(social_dev1, social_dev2)
        registered_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        if connected_status:
            common_orgs = self.get_common_github_orgs(github_devs[0], github_devs[1])
            return DeveloperConnectionStatusOk(registered_at, handle1, handle2, organisations=common_orgs)
        return DeveloperConnectionStatusFalse(registered_at, handle1, handle2)

    @staticmethod
    def get_common_github_orgs(github_dev1: GitHubDeveloper, github_dev2: GitHubDeveloper) -> List[GitHubOrganisation]:
        result = []
        for org in github_dev1.organisations:
            if org in github_dev2.organisations:
                result.append(org)
        return result
