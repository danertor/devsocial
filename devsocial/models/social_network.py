# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
# pylint: disable=no-self-use
from dataclasses import dataclass, asdict
from typing import List, Dict, Union

from devsocial.github.models import GitHubOrganisation
from devsocial.models.base_developer import HandleType


@dataclass
class DeveloperConnectionStatus:
    registered_at: str  # datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    handle1: HandleType
    handle2: HandleType

    def asdict(self) -> Dict[str, str]:
        return asdict(self)


@dataclass
class DeveloperConnectionStatusOk(DeveloperConnectionStatus):
    connected = True
    organisations: List[GitHubOrganisation]

    def asdict(self) -> Dict[str, Union[bool, List[str]]]:
        organisations = [org.name for org in self.organisations]
        return {'connected': self.connected, 'organisations': organisations}


@dataclass
class DeveloperConnectionStatusFalse(DeveloperConnectionStatus):
    connected = False

    def asdict(self) -> Dict[str, bool]:
        return {'connected': self.connected}


@dataclass
class DeveloperConnectionStatusError:
    errors: List[str]

    def asdict(self) -> Dict[str, List[str]]:
        return {'errors': sorted(self.errors)}


@dataclass
class DeveloperConnectionStatusNotFound:
    errors: List[str]

    def asdict(self) -> Dict[str, List[str]]:
        return {'errors': sorted(self.errors)}


@dataclass
class DeveloperConnectionStatusSameHandleError:
    handle: str

    def asdict(self) -> Dict[str, List[str]]:
        return {'errors': ["'handle1' and 'handle2' have the same value", ]}


# Connection History data models
@dataclass
class DeveloperHistoryConnectionStatus:
    registered_at: str  # "%Y-%m-%dT%H:%M:%SZ"

    def asdict(self) -> Dict[str, Union[bool, List[str]]]:
        return asdict(self)


@dataclass
class DeveloperHistoryConnectionStatusOk(DeveloperHistoryConnectionStatus):
    connected = True
    organisations: List[GitHubOrganisation]

    def asdict(self) -> Dict[str, Union[bool, List[str]]]:
        rep_dict = super().asdict()
        rep_dict['organisations'] = [org.name for org in self.organisations]
        rep_dict['connected'] = self.connected
        return rep_dict


@dataclass
class DeveloperHistoryConnectionStatusFalse(DeveloperHistoryConnectionStatus):
    connected = False

    def asdict(self) -> Dict[str, Union[bool, List[str]]]:
        rep_dict = super().asdict()
        rep_dict['connected'] = self.connected
        return rep_dict
