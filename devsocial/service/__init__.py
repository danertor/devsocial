# pylint: disable=missing-class-docstring, missing-function-docstring
# pylint: disable=unused-variable, unused-argument, too-few-public-methods, invalid-name
"""
Contains functions to create singletons objects of the service.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app() -> Flask:
    app = Flask(__name__)
    return app


def create_db_conn(app: Flask = None) -> SQLAlchemy:
    if not app:
        app = create_app()
    db = SQLAlchemy(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = ""  # type postgresql://{username}:{password}@localhost:5432/{dbname}

    return db
