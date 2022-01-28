# pylint: disable=missing-class-docstring, missing-function-docstring, disable=missing-module-docstring
# pylint: disable=no-self-use
from flask import Response, Blueprint
from flask_restx import Api, Namespace, Resource

from devsocial.models.base_developer import HandleType
from .handlers import realtime, register


realtime_namespace = Namespace(
    name='Realtime Connected API',
    description='Check if developers are currently connected',
    path='/'
)


register_namespace = Namespace(
    name='Historical Register Connections API',
    description='Get historical data of developers connections',
    path='/'
)


@realtime_namespace.route('/connected/realtime/<handle1>/<handle2>', methods=['GET'])
class RealtimeEndpointController(Resource):

    def get(self, handle1: HandleType, handle2: HandleType) -> Response:
        response = realtime(handle1, handle2)
        return response


@register_namespace.route('/connected/register/<handle1>/<handle2>', methods=['GET'])
class RegisterEndpointController(Resource):

    def get(self, handle1: HandleType, handle2: HandleType) -> Response:
        response = register(handle1, handle2)
        return response


dev_social_api = Blueprint("DeveloperSocialConnectedApi", __name__)

api = Api(
    dev_social_api,
    version='1.0',
    title='DeveloperSocialConnectedApi',
    description='Social Network API for connected developers',
    doc='/'
)

api.add_namespace(realtime_namespace)
api.add_namespace(register_namespace)
