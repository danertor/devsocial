# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from typing import Dict

from devsocial import config
from devsocial.models.base_developer import BaseDeveloper


class SocialDeveloper(BaseDeveloper):
    """
    It stores all the social accounts of the developer.
    A developer might have zero, some, or all social accounts.
    It assumes a developer can't have more than one account on each social networks.
    It assumes the developer must have the same handle across multiple social accounts.
    """
    def __init__(self, handle: str):
        super().__init__(handle)
        self.accounts: Dict[str, BaseDeveloper] = {}

    @staticmethod
    def check_allowed_account_type(developer_account: BaseDeveloper) -> bool:
        return any(isinstance(developer_account, allowed_cls) for allowed_cls in config.FULLY_CONNECTED_DEVELOPER_TYPES)

    def add_account(self, developer_account: BaseDeveloper) -> None:
        social_developer_type = developer_account.__class__.__name__
        if not self.check_allowed_account_type(developer_account):
            raise TypeError(f"{social_developer_type} is not a valid type. Valid social account types: "
                            f"{', '.join(config.FULLY_CONNECTED_DEVELOPER_TYPE_NAMES)}")

        if developer_account.handle != self.handle:
            raise ValueError("The developer's social accounts must have the same handle.")

        self.accounts[social_developer_type] = developer_account

    def pop_account(self, social_developer_type: str) -> BaseDeveloper:
        return self.accounts.get(social_developer_type)

    def has_account_type(self, developer_type: BaseDeveloper) -> bool:
        return developer_type.__name__ in self.accounts
