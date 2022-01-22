# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from dataclasses import dataclass
from typing import List

from devsocial.github.models import GitHubOrganisation
from devsocial.models.base_developer import HandleType


@dataclass
class DeveloperConnectionStatus:
    registered_at: str  # datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    handle1: HandleType
    handle2: HandleType


@dataclass
class DeveloperConnectionStatusOk(DeveloperConnectionStatus):
    connected = True
    organisations: List[GitHubOrganisation]


@dataclass
class DeveloperConnectionStatusFalse(DeveloperConnectionStatus):
    connected = False


@dataclass
class DeveloperConnectionStatusError(DeveloperConnectionStatus):
    errors: List[str]
