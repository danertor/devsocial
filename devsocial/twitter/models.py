# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from dataclasses import dataclass, field
from typing import List
from devsocial.models.base_developer import BaseDeveloper


TwitterDeveloperIdType = type(str)


@dataclass()
class TwitterDeveloper(BaseDeveloper):
    # pylint: disable=invalid-name
    id: TwitterDeveloperIdType = None
    followers: List[TwitterDeveloperIdType] = field(default_factory=list)
