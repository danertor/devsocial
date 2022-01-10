# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from dataclasses import dataclass, field
from typing import List
from devsocial.models.base_developer import BaseDeveloper


# 'frozen' and 'eq' are set for GitHubOrganization class to be hash-able, thus be an item of a set.
# It is risky to implement a __hash__ function for GitHubOrganization if a developer has many organizations (i.e. +1000)
@dataclass(frozen=True, eq=True)
class GitHubOrganization:
    name: str


@dataclass()
class GitHubDeveloper(BaseDeveloper):
    organizations: List[GitHubOrganization] = field(default_factory=list)
