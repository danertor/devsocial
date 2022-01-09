# pylint: disable:too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
"""
Each social network will have a the business logic implemented in this module.
Note: Please implement the base class methods listed below if you want to create you own social network controller.
"""
from typing import List

from devsocial import config
from devsocial.models.social_developer import SocialDeveloper


# pylint: disable=too-few-public-methods
class DevSocialNet:
    def __init__(self):
        super().__init__()
        self._social_controllers: list = [controller() for controller in config.FULLY_CONNECTED_CONTROLLERS]

    def connected(self, developer1: SocialDeveloper, developer2: SocialDeveloper) -> bool:
        social_connections: List[bool] = []
        for social_controller in self._social_controllers:
            if not developer1.has_account_type(social_controller.developer_type) \
                    or not developer2.has_account_type(social_controller.developer_type):
                return False

            developer1_account = developer1.accounts[social_controller.developer_type_name]
            developer2_account = developer2.accounts[social_controller.developer_type_name]
            social_connections.append(social_controller.connected(developer1_account, developer2_account))
        return all(social_connections)
