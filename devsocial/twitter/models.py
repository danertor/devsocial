# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from dataclasses import dataclass, field
from typing import List
from devsocial.models.base_developer import BaseDeveloper


TwitterDeveloperId = type(str)


@dataclass()
class TwitterDeveloper(BaseDeveloper):
    # pylint: disable=invalid-name
    id: TwitterDeveloperId = None
    followers: List[TwitterDeveloperId] = field(default_factory=list)
