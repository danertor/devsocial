# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from dataclasses import dataclass, field
from typing import List
from .organization import Organization


HandleType = str


@dataclass()
class BaseDeveloper:
    handle: HandleType


@dataclass()
class GitHubDeveloper(BaseDeveloper):
    organizations: List[Organization] = field(default_factory=list)


@dataclass()
class TwitterDeveloper(BaseDeveloper):
    followers: List[BaseDeveloper] = field(default_factory=list)


@dataclass()
class Developer:
    twitter: TwitterDeveloper = field(default=None)
    github: GitHubDeveloper = field(default=None)
