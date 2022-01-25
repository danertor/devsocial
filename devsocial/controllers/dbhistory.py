# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
# pylint: disable=unused-variable, unused-argument, too-few-public-methods
import json
from typing import List

from devsocial.dbmodels.dbhistory import DBDevConnHistoryRow
from devsocial.github.models import GitHubOrganisation
from devsocial.models.base_developer import HandleType
from devsocial.models.social_network import \
    DeveloperConnectionStatus, \
    DeveloperHistoryConnectionStatusOk, \
    DeveloperHistoryConnectionStatusFalse


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
        for row in DBDevConnHistoryRow.query.filter_by(handle1=handle1, handle2=handle2).order_by(DBDevConnHistoryRow.registered_at).all():
            if row.connected:
                organisations = [GitHubOrganisation(name) for name in json.loads(row.organisations)]
                results.append(DeveloperHistoryConnectionStatusOk(row.registered_at, organisations))
            else:
                results.append(DeveloperHistoryConnectionStatusFalse(row.registered_at))
        return results
