# pylint: disable=unused-import
"""
Entrypoint for running the devsocial restfull api service.
Singletons are imported in this module.
"""
from devsocial.service.app import app
from devsocial.dbmodels import db, migrate

import devsocial.service.routes
from devsocial.service.v1.routes import dev_social_api

app.config['DATABASE'] = {}
app.config['DATABASE']['DBNAME'] = 'devsocial_db'
app.config['DATABASE']['PORT'] = 5432
app.config['DATABASE']['HOST'] = 'devsocialdb'
app.config['DATABASE']['USERNAME'] = 'devsocial'
app.config['DATABASE']['PASSWORD'] = 'devsocial'

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{app.config['DATABASE']['USERNAME']}:" \
                                        f"{app.config['DATABASE']['PASSWORD']}" \
                                        f"@{app.config['DATABASE']['HOST']}:" \
                                        f"{app.config['DATABASE']['PORT']}/" \
                                        f"{app.config['DATABASE']['DBNAME']}"
app.config["DEBUG"] = True
app.config["Development"] = True
app.config["LOG_LEVEL"] = "DEBUG"
db.init_app(app)
migrate.init_app(app, db)
app.register_blueprint(dev_social_api, url_prefix='/')

app.run(host='0.0.0.0', port='8080')
