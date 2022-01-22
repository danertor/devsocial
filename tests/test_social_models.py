# pylint: disable=missing-module-docstring, disable=missing-class-docstring, missing-function-docstring
# pylint: disable=unused-variable, unused-argument

import pytest

from devsocial import config
from devsocial.models.social_developer import SocialDeveloper


def test_create_social_developer():
    dev: SocialDeveloper = SocialDeveloper('homer')
    assert dev


def test_add_account_to_social_developer():
    handle = 'homer'
    dev: SocialDeveloper = SocialDeveloper(handle)

    social_developer_account_type = config.FULLY_CONNECTED_DEVELOPER_TYPES[0]
    social_developer_account = social_developer_account_type(handle)

    dev.add_account(social_developer_account)
    assert len(dev.accounts) > 0


def test_add_account_with_different_handle_to_social_developer():
    handle1 = 'homer'
    handle_template = 'hsimpson{}'
    dev: SocialDeveloper = SocialDeveloper(handle1)
    with pytest.raises(ValueError):
        for i, developer_type in enumerate(config.FULLY_CONNECTED_DEVELOPER_TYPES):
            account_handle = handle_template.format(i)
            developer_account = developer_type(account_handle)
            dev.add_account(developer_account)
