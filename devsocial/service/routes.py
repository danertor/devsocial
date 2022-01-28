# pylint: disable=missing-function-docstring
"""
Links to all routes of different versions for backward compatibility
"""
from typing import Dict

from devsocial.dbmodels import db
from .app import app


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/ping')
def ping() -> Dict[str, str]:
    return {'status': 'success'}


@app.route('/health')
def health() -> Dict[str, str]:
    return {'status': 'ok'}


@app.route('/warmup')
def warmup() -> Dict[str, str]:
    return {'status': 'ready'}


@app.route('/ready')
def ready() -> Dict[str, str]:
    return {'status': 'ready'}


@app.route('/live')
@app.route('/liveness')
def live() -> Dict[str, str]:
    return {'status': 'ok'}
