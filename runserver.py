from devsocial.service.app import app
from devsocial.dbmodels import db, migrate
from devsocial.service import routes
from devsocial.service.v1.routes import dev_social_api


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"  # type postgresql://{username}:{password}@localhost:5432/{dbname}
app.config["DEBUG"] = True
app.config["Development"] = True
app.config["LOG_LEVEL"] = "DEBUG"
db.init_app(app)
migrate.init_app(app, db)
# db.create_all()
app.register_blueprint(dev_social_api, url_prefix='/')

app.run(host='localhost', port='8080')
