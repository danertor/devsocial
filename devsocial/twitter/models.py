# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from dataclasses import dataclass, field
from typing import List
from devsocial.models.developer import BaseDeveloper


@dataclass()
class TwitterDeveloper(BaseDeveloper):
    followers: List[BaseDeveloper] = field(default_factory=list)
