"""
Note: Please implement the base class methods listed below if you want to create you own social network controller.
"""
# pylint: disable=missing-function-docstring
from abc import abstractmethod
from flask_sqlalchemy import SQLAlchemy

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
