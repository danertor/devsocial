# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
# pylint: disable=unused-variable, unused-argument, too-few-public-methods
import json

from devsocial.models.social_network import DeveloperConnectionStatus, DeveloperConnectionStatusOk
from devsocial.service.app import db


# basic model
class DBDevConnHistoryRow(db.Model):
    __tablename__ = 'dev_con_history'
    id = db.Column(db.Integer, primary_key=True)
    registered_at = db.Column(db.String())
    handle1 = db.Column(db.String())
    handle2 = db.Column(db.String())
    connected = db.Column(db.Boolean())
    organisations = db.Column(db.String())

    def __init__(self, dev_conn_status: DeveloperConnectionStatus):
        self.registered_at = dev_conn_status.registered_at
        self.handle1 = dev_conn_status.handle1
        self.handle2 = dev_conn_status.handle2
        self.connected = dev_conn_status.connected
        if isinstance(dev_conn_status, DeveloperConnectionStatusOk):
            self.organisations = json.dumps([org.name for org in dev_conn_status.organisations])
        else:
            self.organisations = json.dumps([])
