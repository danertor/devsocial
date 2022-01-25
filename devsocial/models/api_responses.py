# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from dataclasses import dataclass, field
from typing import List, Dict, Union

from social_network import \
    DeveloperHistoryConnectionStatusOk, \
    DeveloperHistoryConnectionStatusFalse, \
    DeveloperConnectionStatusFalse, \
    DeveloperConnectionStatusError, \
    DeveloperConnectionStatusOk


#Realtime
APIResponseRealTimeOK = DeveloperConnectionStatusOk
APIResponseRealTimeFalse = DeveloperConnectionStatusFalse
APIResponseRealTimeError = DeveloperConnectionStatusError


# Register
@dataclass
class APIResponseRegister:
    history: List[Union[DeveloperHistoryConnectionStatusOk, DeveloperHistoryConnectionStatusFalse]] = \
        field(default_factory=list)

    def asdict(self) -> List[Dict]:
        return [his_item.asdict() for his_item in self.history]
