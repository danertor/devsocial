# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from dataclasses import dataclass


# 'frozen' and 'eq' are set for Organization class to be hash-able, thus be an item of a set.
# It is risky to implement a __hash__ function for Organization if a developer has many organizations (i.e. +1000)
@dataclass(frozen=True, eq=True)
class Organization:
    name: str
