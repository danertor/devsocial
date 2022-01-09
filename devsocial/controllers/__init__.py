"""
Behaviours of the different social network classes.
"""
# pylint: disable=missing-function-docstring
from abc import abstractmethod
from devsocial.models.base_developer import BaseDeveloper


# pylint: disable=too-few-public-methods
class BaseSocialController:
    """
    Please inherit from this class in you want to add a new social network controller. i.e. HackerNews controller,...
    To force developers to implement what methods or logic would every social network controller would have.
    """
    def __init__(self):
        pass

    @abstractmethod
    def connected(self, developer1: BaseDeveloper, developer2: BaseDeveloper):
        pass
