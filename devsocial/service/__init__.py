# pylint: disable=missing-class-docstring, missing-function-docstring
# pylint: disable=unused-variable, unused-argument, too-few-public-methods, invalid-name
"""
Contains functions to create singletons objects of the service.
"""
from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    return app
