# pylint: disable=unused-import
"""
Entrypoint for running the devsocial restfull api service.
Singletons are imported in this module.
"""
from devsocial.config import get_os_var
from devsocial.service.app import app
from devsocial.dbmodels import db, migrate

import devsocial.service.routes
from devsocial.service.v1.routes import dev_social_api

try:
    app.config['DATABASE'] = {}
    app.config['DATABASE']['HOST'] = get_os_var('DB_HOST')
    app.config['DATABASE']['DBNAME'] = 'devsocial_db'
    app.config['DATABASE']['PORT'] = 5432
    app.config['DATABASE']['USERNAME'] = 'devsocial'
    app.config['DATABASE']['PASSWORD'] = 'devsocial'
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{app.config['DATABASE']['USERNAME']}:" \
                                            f"{app.config['DATABASE']['PASSWORD']}" \
                                            f"@{app.config['DATABASE']['HOST']}:" \
                                            f"{app.config['DATABASE']['PORT']}/" \
                                            f"{app.config['DATABASE']['DBNAME']}"
except ValueError as _:
    # This it is for showcase purposes. In a real environment,
    # the service should not start if no db config is properly set.
    app.logger.warning('Database environment variables missing, running with on-memory database.')
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"

app.config["DEBUG"] = get_os_var('FLASK_DEBUG', default='False', mandatory=False) == 'True'
app.config["Development"] = app.config["DEBUG"]
app.config["LOG_LEVEL"] = "DEBUG" if app.config["DEBUG"] else 'ERROR'
db.init_app(app)
migrate.init_app(app, db)
app.register_blueprint(dev_social_api, url_prefix='/')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')
