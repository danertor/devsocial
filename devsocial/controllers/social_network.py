# pylint: disable:too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
"""
Each social network will have a the business logic implemented in this module.
Note: Please implement the base class methods listed below if you want to create you own social network controller.
"""
from abc import abstractmethod
from devsocial.models.developer import BaseDeveloper


# pylint: disable=too-few-public-methods
class BaseDevSocialNet:
    def __init__(self):
        pass

    @abstractmethod
    def connected(self, developer1: BaseDeveloper, developer2: BaseDeveloper):
        pass
