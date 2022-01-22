# pylint: disable=missing-class-docstring, missing-function-docstring
# pylint: disable=unused-variable, unused-argument, too-few-public-methods, invalid-name
"""
Location of initialization of service singleton objects.
"""
from flask_migrate import Migrate

from . import create_app, create_db_conn


app = create_app()

db = create_db_conn(app)
migrate = Migrate(app, db)
