# pylint: disable=missing-module-docstring
from devsocial.dbmodels import db
from devsocial.controllers.dbhistory import DBHistoryController
from devsocial.controllers.social_network import DevSocialNet


__version__ = "1.0.0"
__API_version__ = "v1"


social_net: DevSocialNet = DevSocialNet()
db_history_controller = DBHistoryController(db)
