# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from dataclasses import dataclass


HandleType = str


@dataclass()
class BaseDeveloper:
    handle: HandleType
