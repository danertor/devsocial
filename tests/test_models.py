# pylint: disable=missing-module-docstring, missing-function-docstring, unused-variable
import pytest
from devsocial.models.developer import BaseDeveloper


def test_create_developer():
    dev: BaseDeveloper = BaseDeveloper('homer')
    assert dev


# pylint: disable=no-value-for-parameter
def test_fail_developer_with_no_handle():
    with pytest.raises(TypeError):
        empty_dev: BaseDeveloper = BaseDeveloper()


def test_developers_equal():
    dev1: BaseDeveloper = BaseDeveloper('homer')
    dev2: BaseDeveloper = BaseDeveloper('homer')
    assert dev1 == dev2


def test_developers_not_equal():
    dev1: BaseDeveloper = BaseDeveloper('homer')
    dev2: BaseDeveloper = BaseDeveloper('krusty')
    assert dev1 != dev2

    with pytest.raises(AssertionError):
        assert dev1.handle == dev2.handle
