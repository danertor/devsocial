# pylint: disable=missing-module-docstring, disable=missing-class-docstring, missing-function-docstring
# pylint: disable=unused-variable, unused-argument

import pytest
from devsocial.models.base_developer import BaseDeveloper


def test_base_create_basedeveloper():
    dev: BaseDeveloper = BaseDeveloper('homer')
    assert dev


# pylint: disable=no-value-for-parameter
def test_base_fail_developer_with_no_handle():
    with pytest.raises(TypeError):
        empty_dev: BaseDeveloper = BaseDeveloper()


def test_base_developers_equal():
    dev1: BaseDeveloper = BaseDeveloper('homer')
    dev2: BaseDeveloper = BaseDeveloper('homer')
    assert dev1 == dev2


def test_base_basedevelopers_not_equal():
    dev1: BaseDeveloper = BaseDeveloper('homer')
    dev2: BaseDeveloper = BaseDeveloper('krusty')
    assert dev1 != dev2

    with pytest.raises(AssertionError):
        assert dev1.handle == dev2.handle
