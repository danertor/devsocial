# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
# pylint: disable=unused-variable, unused-argument, too-few-public-methods
import json
from typing import List

from devsocial.dbmodels.dbhistory import DBDevConnHistoryRow
from devsocial.github.models import GitHubOrganisation
from devsocial.models.base_developer import HandleType
from devsocial.models.social_network import DeveloperConnectionStatus, DeveloperConnectionStatusOk, \
    DeveloperConnectionStatusFalse


class DBHistoryController:
    """
    For saving or retrieving historical records of developer connections.
    """

    # pylint: disable=invalid-name
    def __init__(self, db):
        self.db = db

    def save_dev_connection(self, dev_conn_status: DeveloperConnectionStatus) -> None:
        new_dev_conn = DBDevConnHistoryRow(dev_conn_status)
        self.db.session.add(new_dev_conn)
        self.db.session.commit()

    def get_dev_connections(self, handle1: HandleType, handle2: HandleType) -> List[DeveloperConnectionStatus]:
        results = []
        for row in self.db.session.query(handle1, handle2):
            if row.connected:
                organisations = [GitHubOrganisation(name) for name in json.loads(row.organisations)]
                results.append(DeveloperConnectionStatusOk(row.registered_at, row.handle1, row.handle2, organisations))
            else:
                results.append(
                    DeveloperConnectionStatusFalse(row.registered_at, row.handle1, row.handle2))
        return results
