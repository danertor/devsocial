# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-few-public-methods
"""
Our Interface for Twitter.
"""
import logging
import traceback
from typing import List
from github import Github, UnknownObjectException

from devsocial import config
from .models import GitHubDeveloper, GitHubOrganisation
from ..exceptions import InvalidHandleError


logger = logging.getLogger()


GitHubApiType = type(Github)


def create_api() -> GitHubApiType:
    return Github(config.GITHUB_API['TOKEN'])


class GitHubApiConnector:
    fields_to_retrieve = 'id'

    def __init__(self, api: GitHubApiType = None):
        self.external_api = api if api else create_api()
        self.config = config.GITHUB_API

    def get_user(self, handle: str) -> GitHubDeveloper:
        try:
            return GitHubDeveloper(handle, organisations=self.get_users_orgs(handle))
        except UnknownObjectException as _:
            raise InvalidHandleError(f"{handle} is no a valid user in github")
        except Exception as _:
            logger.error(traceback.format_exc())
            raise InvalidHandleError(f"Can not get data from github for {handle}")

    def get_users_orgs(self, handle: str) -> List[GitHubOrganisation]:
        organisations = []
        user = self.external_api.get_user(handle)
        fetched_orgs = user.get_orgs()
        for org in fetched_orgs:
            organisations.append(GitHubOrganisation(org.login if org.login else org.name))
        return organisations
