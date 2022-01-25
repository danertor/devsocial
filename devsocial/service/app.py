# pylint: disable=missing-class-docstring, missing-function-docstring
# pylint: disable=unused-variable, unused-argument, too-few-public-methods, invalid-name
"""
Location of initialization of service singleton objects.
"""
import logging

from . import create_app


app = create_app()
app.logger.setLevel(logging.ERROR)
