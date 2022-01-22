# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from dataclasses import dataclass, field
from typing import List
from devsocial.models.base_developer import BaseDeveloper


# 'frozen' and 'eq' are set for GitHubOrganisation class to be hash-able, thus be an item of a set.
# It is risky to implement a __hash__ function for GitHubOrganisation if a developer has many organisations (i.e. +1000)
@dataclass(frozen=True, eq=True)
class GitHubOrganisation:
    name: str


@dataclass()
class GitHubDeveloper(BaseDeveloper):
    organisations: List[GitHubOrganisation] = field(default_factory=list)
