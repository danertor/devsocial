# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-few-public-methods
"""
Our Interface for Twitter.
"""
from typing import List
from github import Github

from devsocial import config
from .models import GitHubDeveloper, GitHubOrganization


def create_api() -> Github:
    return Github(config.GITHUB_API['TOKEN'])


class GitHubApiConnector:
    fields_to_retrieve = 'id'

    def __init__(self, api: Github):
        self.external_api = api
        self.config = config.GITHUB_API

    def get_user(self, handle: str) -> GitHubDeveloper:
        return GitHubDeveloper(handle, organizations=self.get_users_orgs(handle))

    def get_users_orgs(self, handle: str) -> List[GitHubOrganization]:
        organizations = []
        user = self.external_api.get_user(handle)
        fetched_orgs = user.get_orgs()
        for org in fetched_orgs:
            organizations.append(GitHubOrganization(org.login))
        return organizations
