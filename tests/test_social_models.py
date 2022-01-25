# pylint: disable=missing-module-docstring, disable=missing-class-docstring, missing-function-docstring
# pylint: disable=unused-variable, unused-argument
import pytest

from devsocial import config
from devsocial.github.models import GitHubOrganisation
from devsocial.models.social_developer import SocialDeveloper
from devsocial.models.social_network import DeveloperHistoryConnectionStatusFalse, DeveloperHistoryConnectionStatusOk, \
    DeveloperConnectionStatusError


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


def test_dev_conn_status_error_dict():
    handle_1 = 'dev1'
    handle_2 = 'dev2'
    error_msgs = [f"{handle_1} is no a valid user in github",
                  f"{handle_1} is no a valid user in twitter",
                  f"{handle_2} is no a valid user in twitter"
                  ]
    dev_conn_status_error = DeveloperConnectionStatusError(errors=error_msgs)
    expected = {
        "errors": [
            f"{handle_1} is no a valid user in github",
            f"{handle_1} is no a valid user in twitter",
            f"{handle_2} is no a valid user in twitter"
        ]
    }
    assert dev_conn_status_error.asdict() == expected


# History connections
def test_dev_history_conn_status_ok_asdict():
    registered_at = "2022-01-25T17:55:10Z"
    organisation_names = ("Nuclear Plant", "Moe's Tavern")
    organisations = [GitHubOrganisation(name) for name in organisation_names]
    dev_conn_status_ok = DeveloperHistoryConnectionStatusOk(registered_at, organisations=organisations)
    expected = {'connected': True, 'organisations': list(organisation_names)}
    assert dev_conn_status_ok.asdict() == expected


def test_dev_history_conn_status_false_asdict():
    registered_at = "2022-01-25T17:55:10Z"
    dev_conn_status_false = DeveloperHistoryConnectionStatusFalse(registered_at)
    expected = {'connected': False, 'registered_at': registered_at}
    assert dev_conn_status_false.asdict() == expected
