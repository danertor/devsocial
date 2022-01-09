# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from dataclasses import dataclass, field
from typing import List
from devsocial.models.base_developer import BaseDeveloper
from devsocial.models.organization import Organization


@dataclass()
class GitHubDeveloper(BaseDeveloper):
    organizations: List[Organization] = field(default_factory=list)
