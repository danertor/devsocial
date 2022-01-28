# pylint: disable=missing-class-docstring, missing-function-docstring, disable=missing-module-docstring

from typing import List

from flask import Response, make_response, jsonify

from devsocial.dbmodels import db
from devsocial.controllers.dbhistory import DBHistoryController
from devsocial.models.base_developer import HandleType
from devsocial.controllers.social_network import DevSocialNet
from devsocial.models.social_network import DeveloperConnectionStatus, DeveloperConnectionStatusOk, \
    DeveloperConnectionStatusFalse, DeveloperConnectionStatusNotFound, DeveloperConnectionStatusSameHandleError

social_net: DevSocialNet = DevSocialNet()
db_history_controller = DBHistoryController(db)


def realtime(handle1: HandleType, handle2: HandleType) -> Response:
    result: DeveloperConnectionStatus = social_net.handles_connected(handle1, handle2)
    response = jsonify(result.asdict())

    if isinstance(result, DeveloperConnectionStatusSameHandleError):
        return make_response(response, 400)

    if isinstance(result, DeveloperConnectionStatusNotFound):
        return make_response(response, 404)

    if isinstance(result, (DeveloperConnectionStatusOk, DeveloperConnectionStatusFalse)):
        db_history_controller.save_dev_connection(result)
        return make_response(response, 200)

    return make_response("Internal Server Error", 500)


def register(handle1: HandleType, handle2: HandleType) -> Response:
    db_results: List[DeveloperConnectionStatus] = db_history_controller.get_dev_connections(handle1, handle2)
    if not db_results:
        return make_response({'errors': [f"No connection registers found for '{handle1}' and '{handle2}'", ]}, 404)
    response = jsonify([item.asdict() for item in db_results])
    return make_response(response, 200)
